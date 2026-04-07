"""
FastAPI application for the Customer Support Environment.

Exposes the SupportEnvironment over HTTP endpoints:
    POST /reset  — Start a new episode
    POST /step   — Execute an action
    GET  /state  — Get current episode state
    GET  /health — Health check

Usage:
    uvicorn env.server.app:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any

from env.server.support_environment import SupportEnvironment
from env.models import SupportAction


# ═══════════════════════════════════════════════════════════════════════════
# Pydantic request models (for OpenAPI docs / validation)
# ═══════════════════════════════════════════════════════════════════════════


class ResetRequest(BaseModel):
    seed: Optional[int] = None
    episode_id: Optional[str] = None
    task_level: Optional[str] = None


class StepRequest(BaseModel):
    action_type: str
    category: Optional[str] = None
    message: Optional[str] = None
    team: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════
# App setup
# ═══════════════════════════════════════════════════════════════════════════


app = FastAPI(
    title="Customer Support Ticket Resolution Environment",
    description=(
        "An OpenEnv-compatible environment for training AI agents to "
        "handle customer support tickets end-to-end."
    ),
    version="1.0.0",
)

# Allow CORS for local development & external clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single environment instance (stateful, sequential episodes)
env = SupportEnvironment()


# ═══════════════════════════════════════════════════════════════════════════
# Endpoints
# ═══════════════════════════════════════════════════════════════════════════


@app.post("/reset")
async def reset(payload: ResetRequest = ResetRequest()) -> Dict[str, Any]:
    """
    Reset the environment and start a new episode.

    Optionally specify a task_level ('easy', 'medium', 'hard')
    and a seed for reproducibility.
    """
    obs = env.reset(
        seed=payload.seed,
        episode_id=payload.episode_id,
        task_level=payload.task_level,
    )
    return obs.model_dump()


@app.post("/step")
async def step(payload: StepRequest) -> Dict[str, Any]:
    """
    Execute an action in the environment.

    action_type must be one of:
      classify_issue, reply, escalate, resolve, request_more_info
    """
    action = SupportAction(
        action_type=payload.action_type,
        category=payload.category,
        message=payload.message,
        team=payload.team,
    )
    obs = env.step(action)
    return obs.model_dump()


@app.get("/state")
async def state() -> Dict[str, Any]:
    """Return the current episode state."""
    return env.state.model_dump()


@app.get("/health")
async def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "environment": "customer-support-env"}


# ═══════════════════════════════════════════════════════════════════════════
# Direct execution
# ═══════════════════════════════════════════════════════════════════════════


def main():
    """Run the server directly (without Docker)."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
