"""
Data models for the Customer Support Ticket Resolution Environment.

Defines Action, Observation, State, and Reward using Pydantic BaseModel,
compatible with the OpenEnv framework's type system.
"""

from pydantic import BaseModel, Field
from typing import ClassVar, Optional, List, Dict, Any, Set


# ---------------------------------------------------------------------------
# Action
# ---------------------------------------------------------------------------


class SupportAction(BaseModel):
    """
    An action the agent can take in the support environment.

    Attributes:
        action_type: One of 'classify_issue', 'reply', 'escalate',
                     'resolve', 'request_more_info'.
        category:    Required for 'classify_issue'. One of 'billing',
                     'technical', 'account', 'general'.
        message:     Required for 'reply'. The response text to send.
        team:        Required for 'escalate'. One of 'billing_team',
                     'technical_team', 'management', 'security_team'.
    """

    action_type: str
    category: Optional[str] = None
    message: Optional[str] = None
    team: Optional[str] = None

    # ---- Class-level constants for valid values --------------------------
    VALID_ACTION_TYPES: ClassVar[Set[str]] = {"classify_issue", "reply", "escalate", "resolve", "request_more_info"}
    VALID_CATEGORIES: ClassVar[Set[str]] = {"billing", "technical", "account", "general"}
    VALID_TEAMS: ClassVar[Set[str]] = {"billing_team", "technical_team", "management", "security_team"}

    def validate_action(self) -> Optional[str]:
        """Return an error string if the action is invalid, else None."""
        if self.action_type not in self.VALID_ACTION_TYPES:
            return (
                f"Invalid action_type '{self.action_type}'. "
                f"Must be one of {self.VALID_ACTION_TYPES}"
            )

        if self.action_type == "classify_issue":
            if not self.category:
                return "classify_issue requires a 'category' field."
            if self.category not in self.VALID_CATEGORIES:
                return (
                    f"Invalid category '{self.category}'. "
                    f"Must be one of {self.VALID_CATEGORIES}"
                )

        if self.action_type == "reply":
            if not self.message or not self.message.strip():
                return "reply requires a non-empty 'message' field."

        if self.action_type == "escalate":
            if not self.team:
                return "escalate requires a 'team' field."
            if self.team not in self.VALID_TEAMS:
                return (
                    f"Invalid team '{self.team}'. "
                    f"Must be one of {self.VALID_TEAMS}"
                )

        return None


# ---------------------------------------------------------------------------
# Observation
# ---------------------------------------------------------------------------


class SupportObservation(BaseModel):
    """
    Observation returned by the environment after each step.

    Provides the agent with everything it needs to decide its next action.
    """

    # Ticket info
    ticket_id: str = ""
    ticket_text: str = ""
    customer_name: str = ""
    customer_priority: str = "medium"          # low | medium | high | critical
    customer_history: List[str] = Field(default_factory=list)

    # Conversation state
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)
    ticket_status: str = "open"                # open | classified | in_progress | escalated | resolved

    # Task metadata
    goal: str = ""
    current_task: str = ""                     # easy | medium | hard

    # OpenEnv-standard fields
    done: bool = False
    reward: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------


class SupportState(BaseModel):
    """
    Internal episode state tracked by the environment.

    Includes OpenEnv-standard fields (episode_id, step_count) plus
    domain-specific tracking fields used by graders.
    """

    # OpenEnv-standard
    episode_id: str = ""
    step_count: int = 0

    # Domain-specific tracking
    accumulated_reward: float = 0.0
    actions_taken: List[str] = Field(default_factory=list)
    current_category: Optional[str] = None
    is_escalated: bool = False
    is_resolved: bool = False
    classification_correct: bool = False
    asked_clarification: bool = False
    replied_helpfully: bool = False
    empathetic_response: bool = False
    urgency_detected: bool = False
    escalation_team: Optional[str] = None


# ---------------------------------------------------------------------------
# Reward
# ---------------------------------------------------------------------------


class SupportReward(BaseModel):
    """
    Reward signal returned by the environment after each step.

    Provides both the step reward and accumulated episode reward,
    along with a breakdown of reward components for interpretability.
    """

    step_reward: float = 0.0
    accumulated_reward: float = 0.0
    components: Dict[str, float] = Field(default_factory=dict)
    description: str = ""
