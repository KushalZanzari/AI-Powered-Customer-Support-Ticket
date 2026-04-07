"""
Deterministic graders for the Customer Support Environment.

Each grader returns a score in [0.0, 1.0].
Scoring is purely keyword/state-based — no LLM calls, no randomness.
"""

from typing import Dict, Any, List, Optional

from env.models import SupportState


# ═══════════════════════════════════════════════════════════════════════════
# Helper utilities
# ═══════════════════════════════════════════════════════════════════════════


def _keywords_present(text: str, keywords: List[str], threshold: int = 2) -> bool:
    """Check whether at least *threshold* keywords appear in *text*."""
    text_lower = text.lower()
    matches = sum(1 for kw in keywords if kw.lower() in text_lower)
    return matches >= threshold


def _any_keyword_present(text: str, keywords: List[str]) -> bool:
    """Check whether any keyword appears in *text*."""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def _get_agent_replies(state: SupportState, conversation: List[Dict[str, str]]) -> str:
    """Concatenate all agent replies into a single string for analysis."""
    replies = [
        msg.get("content", "")
        for msg in conversation
        if msg.get("role") == "agent"
    ]
    return " ".join(replies)


# ═══════════════════════════════════════════════════════════════════════════
# Task 1 — Easy: Basic FAQ Resolution
# ═══════════════════════════════════════════════════════════════════════════


def grade_easy(
    state: SupportState,
    ticket: Dict[str, Any],
    conversation: List[Dict[str, str]],
) -> float:
    """
    Grade a basic FAQ resolution attempt.

    Scoring breakdown (0.0 – 1.0):
        +0.3 — Correct issue classification
        +0.4 — Helpful reply (contains relevant keywords)
        +0.3 — Ticket resolved

    Args:
        state:        The final environment state.
        ticket:       The ticket data dictionary.
        conversation: The full conversation history.

    Returns:
        A deterministic score between 0.0 and 1.0.
    """
    score = 0.0

    # --- 0.3  Correct classification ---
    if state.classification_correct:
        score += 0.3

    # --- 0.4  Helpful reply ---
    agent_text = _get_agent_replies(state, conversation)
    resolution_kw = ticket.get("expected_resolution_keywords", [])
    if _keywords_present(agent_text, resolution_kw, threshold=2):
        score += 0.4

    # --- 0.3  Resolved ---
    if state.is_resolved:
        score += 0.3

    return round(min(score, 1.0), 2)


# ═══════════════════════════════════════════════════════════════════════════
# Task 2 — Medium: Multi-step Issue Handling
# ═══════════════════════════════════════════════════════════════════════════


def grade_medium(
    state: SupportState,
    ticket: Dict[str, Any],
    conversation: List[Dict[str, str]],
) -> float:
    """
    Grade a multi-step issue handling attempt.

    Scoring breakdown (0.0 – 1.0):
        +0.25 — Correct issue classification
        +0.25 — Asked for clarification / more info
        +0.30 — Provided a correct solution (keyword match)
        +0.20 — Ticket resolved

    Args:
        state:        The final environment state.
        ticket:       The ticket data dictionary.
        conversation: The full conversation history.

    Returns:
        A deterministic score between 0.0 and 1.0.
    """
    score = 0.0

    # --- 0.25  Correct classification ---
    if state.classification_correct:
        score += 0.25

    # --- 0.25  Asked for clarification ---
    if state.asked_clarification:
        score += 0.25

    # --- 0.30  Correct solution ---
    agent_text = _get_agent_replies(state, conversation)
    resolution_kw = ticket.get("expected_resolution_keywords", [])
    if _keywords_present(agent_text, resolution_kw, threshold=2):
        score += 0.30

    # --- 0.20  Resolved ---
    if state.is_resolved:
        score += 0.20

    return round(min(score, 1.0), 2)


# ═══════════════════════════════════════════════════════════════════════════
# Task 3 — Hard: Complex Escalation Case
# ═══════════════════════════════════════════════════════════════════════════


def grade_hard(
    state: SupportState,
    ticket: Dict[str, Any],
    conversation: List[Dict[str, str]],
) -> float:
    """
    Grade a complex escalation case.

    Scoring breakdown (0.0 – 1.0):
        +0.20 — Empathetic response (tone keywords)
        +0.20 — Urgency detected correctly
        +0.20 — Correct issue classification
        +0.20 — Correct escalation team
        +0.20 — Resolved or properly escalated

    Args:
        state:        The final environment state.
        ticket:       The ticket data dictionary.
        conversation: The full conversation history.

    Returns:
        A deterministic score between 0.0 and 1.0.
    """
    score = 0.0

    agent_text = _get_agent_replies(state, conversation)

    # --- 0.20  Empathetic response ---
    empathy_kw = ticket.get("empathy_keywords", [])
    if _any_keyword_present(agent_text, empathy_kw):
        score += 0.20

    # --- 0.20  Urgency detected ---
    if state.urgency_detected:
        score += 0.20

    # --- 0.20  Correct classification ---
    if state.classification_correct:
        score += 0.20

    # --- 0.20  Correct escalation ---
    expected_team = ticket.get("expected_escalation_team")
    if expected_team and state.escalation_team == expected_team:
        score += 0.20

    # --- 0.20  Resolved / properly escalated ---
    if state.is_resolved or state.is_escalated:
        score += 0.20

    return round(min(score, 1.0), 2)
