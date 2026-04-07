"""
Customer Support Ticket Resolution — Core Environment Logic.

Implements the OpenEnv-compatible Environment with step(), reset(), and
state() for handling customer support tickets across three difficulty levels.
"""

import random
import uuid
from typing import Any, Dict, List, Optional

from env.models import SupportAction, SupportObservation, SupportState
from env.graders import grade_easy, grade_medium, grade_hard
from env.ticket_data import get_tickets_by_level


# Maximum steps before the episode is forcefully terminated.
MAX_STEPS = 8


class SupportEnvironment:
    """
    AI-Powered Customer Support Ticket Resolution Environment.

    The agent interacts with realistic customer support tickets using
    five action types: classify_issue, reply, escalate, resolve, and
    request_more_info.

    Rewards are shaped per-step and a final deterministic grade is
    computed at episode end.
    """

    def __init__(self) -> None:
        self._state = SupportState()
        self._ticket: Dict[str, Any] = {}
        self._conversation: List[Dict[str, str]] = []
        self._task_level: str = "easy"
        self._observation: Optional[SupportObservation] = None

    # ──────────────────────────────────────────────────────────────────────
    # reset
    # ──────────────────────────────────────────────────────────────────────

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        task_level: Optional[str] = None,
        **kwargs: Any,
    ) -> SupportObservation:
        """
        Start a new episode.

        Args:
            seed:       Optional random seed for reproducibility.
            episode_id: Optional episode identifier.
            task_level: One of 'easy', 'medium', 'hard'.
                        Defaults to random selection.
        """
        if seed is not None:
            random.seed(seed)

        # Choose task level
        self._task_level = task_level or random.choice(["easy", "medium", "hard"])
        tickets = get_tickets_by_level(self._task_level)
        self._ticket = random.choice(tickets)

        # Fresh state
        self._state = SupportState(
            episode_id=episode_id or str(uuid.uuid4()),
            step_count=0,
        )
        self._conversation = []

        # Build initial observation
        self._observation = SupportObservation(
            ticket_id=self._ticket["ticket_id"],
            ticket_text=self._ticket["ticket_text"],
            customer_name=self._ticket["customer_name"],
            customer_priority=self._ticket["customer_priority"],
            customer_history=self._ticket.get("customer_history", []),
            conversation_history=[],
            ticket_status="open",
            goal=self._ticket["goal"],
            current_task=self._task_level,
            done=False,
            reward=0.0,
            metadata={"message": "Environment reset. New ticket assigned."},
        )

        return self._observation

    # ──────────────────────────────────────────────────────────────────────
    # step
    # ──────────────────────────────────────────────────────────────────────

    def step(self, action: SupportAction, **kwargs: Any) -> SupportObservation:
        """
        Execute an agent action and return the next observation.

        Handles validation, reward shaping, conversation tracking,
        termination checks, and final grading.
        """
        self._state.step_count += 1

        # ── validate ─────────────────────────────────────────────────────
        error = action.validate_action()
        if error:
            return self._make_observation(
                reward=-0.2,
                metadata={"error": error},
            )

        # ── guard: already done ──────────────────────────────────────────
        if self._state.is_resolved:
            return self._make_observation(
                reward=-1.0,
                done=True,
                metadata={"error": "Ticket is already resolved."},
            )

        # ── loop detection (same action repeated ≥ 3 times) ─────────────
        self._state.actions_taken.append(action.action_type)
        if len(self._state.actions_taken) >= 3:
            last_three = self._state.actions_taken[-3:]
            if len(set(last_three)) == 1:
                return self._make_observation(
                    reward=-1.0,
                    done=True,
                    metadata={"error": "Infinite loop detected — same action repeated 3 times."},
                )

        # ── dispatch action handler ──────────────────────────────────────
        handler = {
            "classify_issue": self._handle_classify,
            "reply": self._handle_reply,
            "escalate": self._handle_escalate,
            "resolve": self._handle_resolve,
            "request_more_info": self._handle_request_more_info,
        }.get(action.action_type)

        reward, metadata = handler(action)  # type: ignore[misc]
        self._state.accumulated_reward += reward

        # ── check termination ────────────────────────────────────────────
        done = self._state.is_resolved or self._state.step_count >= MAX_STEPS

        # ── final grading on episode end ─────────────────────────────────
        if done:
            final_score = self._run_grader()
            metadata["final_score"] = final_score
            metadata["task_level"] = self._task_level

        return self._make_observation(reward=reward, done=done, metadata=metadata)

    # ──────────────────────────────────────────────────────────────────────
    # state property
    # ──────────────────────────────────────────────────────────────────────

    @property
    def state(self) -> SupportState:
        """Return the current episode state."""
        return self._state

    # ══════════════════════════════════════════════════════════════════════
    # Action Handlers (private)
    # ══════════════════════════════════════════════════════════════════════

    def _handle_classify(self, action: SupportAction) -> tuple:
        """Handle a classify_issue action."""
        expected = self._ticket.get("expected_category", "")
        correct = action.category == expected

        self._state.current_category = action.category
        self._state.classification_correct = correct

        self._conversation.append({
            "role": "agent",
            "action": "classify_issue",
            "content": f"Classified as: {action.category}",
        })

        if correct:
            reward = 0.5
            msg = f"Correct classification: {action.category}"
        else:
            reward = -0.2
            msg = (
                f"Incorrect classification: {action.category} "
                f"(expected: {expected})"
            )

        return reward, {"classification": msg}

    def _handle_reply(self, action: SupportAction) -> tuple:
        """Handle a reply action."""
        message = action.message or ""
        self._conversation.append({
            "role": "agent",
            "action": "reply",
            "content": message,
        })

        # Check reply quality against expected keywords
        resolution_kw = self._ticket.get("expected_resolution_keywords", [])
        text_lower = message.lower()
        kw_hits = sum(1 for kw in resolution_kw if kw.lower() in text_lower)

        # Empathy check (for hard tasks)
        empathy_kw = self._ticket.get("empathy_keywords", [])
        if empathy_kw and any(kw.lower() in text_lower for kw in empathy_kw):
            self._state.empathetic_response = True

        # Urgency detection (for hard tasks)
        urgency_kw = self._ticket.get("urgency_indicators", [])
        if urgency_kw:
            # Agent acknowledges urgency if they mention related terms
            urgency_acknowledge = [
                "priority", "urgent", "immediately", "right away",
                "escalat", "highest priority", "p0", "critical",
            ]
            if any(term in text_lower for term in urgency_acknowledge):
                self._state.urgency_detected = True

        if kw_hits >= 2:
            self._state.replied_helpfully = True
            reward = 0.5
            msg = f"Helpful reply — {kw_hits} relevant keywords matched."
        elif kw_hits == 1:
            reward = 0.2
            msg = "Partially helpful reply — 1 keyword matched."
        else:
            reward = -0.5
            msg = "Reply lacked relevant content — 0 keywords matched."

        return reward, {"reply_quality": msg}

    def _handle_escalate(self, action: SupportAction) -> tuple:
        """Handle an escalate action."""
        self._state.is_escalated = True
        self._state.escalation_team = action.team

        self._conversation.append({
            "role": "agent",
            "action": "escalate",
            "content": f"Escalated to: {action.team}",
        })

        expected_team = self._ticket.get("expected_escalation_team")

        if expected_team and action.team == expected_team:
            reward = 0.5
            msg = f"Correct escalation to {action.team}."
        elif expected_team:
            reward = 0.1
            msg = (
                f"Escalated to {action.team}, but expected "
                f"{expected_team}."
            )
        else:
            # Ticket didn't need escalation
            reward = -0.2
            msg = "Unnecessary escalation — this ticket could be resolved directly."

        return reward, {"escalation": msg}

    def _handle_resolve(self, action: SupportAction) -> tuple:
        """Handle a resolve action."""
        self._conversation.append({
            "role": "agent",
            "action": "resolve",
            "content": "Ticket resolved.",
        })

        # Check if the agent has done enough work first
        has_replied = any(
            m.get("action") == "reply" for m in self._conversation
        )

        if has_replied:
            self._state.is_resolved = True
            reward = 1.0
            msg = "Ticket resolved successfully."
        else:
            # Resolving without any reply is a bad practice
            self._state.is_resolved = True
            reward = 0.2
            msg = "Ticket resolved, but no reply was sent to the customer."

        return reward, {"resolution": msg}

    def _handle_request_more_info(self, action: SupportAction) -> tuple:
        """Handle a request_more_info action."""
        self._state.asked_clarification = True

        self._conversation.append({
            "role": "agent",
            "action": "request_more_info",
            "content": "Requested additional information from the customer.",
        })

        # Simulate a customer response with relevant context
        customer_response = self._simulate_customer_response()
        self._conversation.append({
            "role": "customer",
            "action": "response",
            "content": customer_response,
        })

        reward = 0.3
        msg = "Good — gathered more information from the customer."
        return reward, {"info_request": msg, "customer_response": customer_response}

    # ══════════════════════════════════════════════════════════════════════
    # Internals
    # ══════════════════════════════════════════════════════════════════════

    def _simulate_customer_response(self) -> str:
        """Generate a simulated customer response to an info request."""
        level = self._task_level
        ticket = self._ticket

        if level == "medium":
            clarification_kw = ticket.get("clarification_keywords", [])
            details = ", ".join(clarification_kw[:3]) if clarification_kw else "additional details"
            return (
                f"Sure, here are the details you asked about: {details}. "
                f"Please let me know if you need anything else."
            )
        elif level == "hard":
            return (
                "I just need this fixed as soon as possible. "
                "I've attached screenshots and logs. Please hurry."
            )
        else:
            return "Thanks for looking into this. Let me know if you need more info."

    def _make_observation(
        self,
        reward: float = 0.0,
        done: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SupportObservation:
        """Build a SupportObservation from the current state."""
        # Determine ticket status
        if self._state.is_resolved:
            status = "resolved"
        elif self._state.is_escalated:
            status = "escalated"
        elif self._state.current_category:
            status = "classified"
        else:
            status = "open"

        obs = SupportObservation(
            ticket_id=self._ticket.get("ticket_id", ""),
            ticket_text=self._ticket.get("ticket_text", ""),
            customer_name=self._ticket.get("customer_name", ""),
            customer_priority=self._ticket.get("customer_priority", "medium"),
            customer_history=self._ticket.get("customer_history", []),
            conversation_history=list(self._conversation),
            ticket_status=status,
            goal=self._ticket.get("goal", ""),
            current_task=self._task_level,
            done=done,
            reward=reward,
            metadata=metadata or {},
        )
        self._observation = obs
        return obs

    def _run_grader(self) -> float:
        """Run the appropriate grader and return the final score."""
        graders = {
            "easy": grade_easy,
            "medium": grade_medium,
            "hard": grade_hard,
        }
        grader = graders.get(self._task_level, grade_easy)
        return grader(self._state, self._ticket, self._conversation)
