"""
Customer Support Environment — HTTP Client.

Provides a simple synchronous client that talks to the FastAPI server
over HTTP.  Can be used standalone or inside RL training loops.

Usage:
    >>> from env.client import SupportEnvClient
    >>> client = SupportEnvClient("http://localhost:8000")
    >>> obs = client.reset(task_level="easy")
    >>> obs = client.step("classify_issue", category="account")
    >>> obs = client.step("reply", message="Here are the instructions…")
    >>> obs = client.step("resolve")
    >>> print(obs["metadata"]["final_score"])
"""

import requests
from typing import Optional, Dict, Any


class SupportEnvClient:
    """
    Synchronous HTTP client for the Customer Support Environment.

    Wraps the /reset, /step, /state, and /health endpoints.
    """

    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    # ──────────────────────────────────────────────────────────────────────
    # Core API
    # ──────────────────────────────────────────────────────────────────────

    def reset(
        self,
        task_level: Optional[str] = None,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Start a new episode and return the initial observation."""
        payload: Dict[str, Any] = {}
        if task_level:
            payload["task_level"] = task_level
        if seed is not None:
            payload["seed"] = seed
        if episode_id:
            payload["episode_id"] = episode_id

        resp = self.session.post(f"{self.base_url}/reset", json=payload)
        resp.raise_for_status()
        return resp.json()

    def step(
        self,
        action_type: str,
        category: Optional[str] = None,
        message: Optional[str] = None,
        team: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute an action and return the resulting observation."""
        payload: Dict[str, Any] = {"action_type": action_type}
        if category:
            payload["category"] = category
        if message:
            payload["message"] = message
        if team:
            payload["team"] = team

        resp = self.session.post(f"{self.base_url}/step", json=payload)
        resp.raise_for_status()
        return resp.json()

    def state(self) -> Dict[str, Any]:
        """Return the current episode state."""
        resp = self.session.get(f"{self.base_url}/state")
        resp.raise_for_status()
        return resp.json()

    def health(self) -> Dict[str, str]:
        """Check if the server is healthy."""
        resp = self.session.get(f"{self.base_url}/health")
        resp.raise_for_status()
        return resp.json()

    # ──────────────────────────────────────────────────────────────────────
    # Context manager support
    # ──────────────────────────────────────────────────────────────────────

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.session.close()

    def close(self):
        """Close the underlying HTTP session."""
        self.session.close()
