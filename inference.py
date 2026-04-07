"""
Baseline Inference Script for the Customer Support Environment.

Uses the OpenAI-compatible client to interact with an LLM, which acts
as the AI agent solving customer support tickets.

Required environment variables:
    API_BASE_URL  — Base URL of the LLM API (e.g., vLLM, TGI, OpenAI)
    MODEL_NAME    — Model identifier
    HF_TOKEN      — HuggingFace token (or API_KEY for OpenAI)

Usage:
    export API_BASE_URL="https://api.openai.com/v1"
    export MODEL_NAME="gpt-4"
    export HF_TOKEN="sk-..."
    python inference.py
"""

import json
import os
import sys
import re
import time
from typing import Any, Dict, List, Optional

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed.  Run: pip install openai")
    sys.exit(1)

import requests


# ═══════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")

ENV_URL = os.getenv("ENV_URL", "http://localhost:8000")

# Initialise LLM client
client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)


# ═══════════════════════════════════════════════════════════════════════════
# Structured logging helpers — [START], [STEP], [END]
# ═══════════════════════════════════════════════════════════════════════════


def log_start(task: str, ticket_id: str, customer_name: str,
              customer_priority: str, goal: str) -> None:
    """Emit a [START] log line at the beginning of an episode."""
    payload = {
        "task": task,
        "ticket_id": ticket_id,
        "customer_name": customer_name,
        "customer_priority": customer_priority,
        "goal": goal,
        "model": MODEL_NAME,
        "timestamp": time.time(),
    }
    print(f"[START] {json.dumps(payload)}")


def log_step(step: int, action: Dict[str, Any], reward: float,
             done: bool, ticket_status: str) -> None:
    """Emit a [STEP] log line after each environment step."""
    payload = {
        "step": step,
        "action": action,
        "reward": reward,
        "done": done,
        "ticket_status": ticket_status,
        "timestamp": time.time(),
    }
    print(f"[STEP] {json.dumps(payload)}")


def log_end(task: str, ticket_id: str, final_score: float,
            total_steps: int, accumulated_reward: float) -> None:
    """Emit an [END] log line at the end of an episode."""
    payload = {
        "task": task,
        "ticket_id": ticket_id,
        "final_score": final_score,
        "total_steps": total_steps,
        "accumulated_reward": accumulated_reward,
        "model": MODEL_NAME,
        "timestamp": time.time(),
    }
    print(f"[END] {json.dumps(payload)}")


# ═══════════════════════════════════════════════════════════════════════════
# Action parsing
# ═══════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """\
You are an expert customer support agent. You handle support tickets by
taking structured actions. You must respond with EXACTLY ONE JSON action
object per turn.

Available actions:
  {"action_type": "classify_issue", "category": "<billing|technical|account|general>"}
  {"action_type": "reply", "message": "<your message to the customer>"}
  {"action_type": "escalate", "team": "<billing_team|technical_team|management|security_team>"}
  {"action_type": "resolve"}
  {"action_type": "request_more_info"}

Rules:
1. Always classify the issue before replying.
2. For simple questions, classify → reply → resolve.
3. For complex issues, classify → request_more_info → reply → resolve.
4. For angry/critical customers, reply empathetically first → classify → escalate → resolve.
5. Match your response to the urgency and tone of the customer.
6. Return ONLY the JSON action, no other text.
"""


def parse_action(llm_output: str) -> Dict[str, Any]:
    """
    Extract a JSON action from the LLM's response.

    Tries direct JSON parsing first, then falls back to regex extraction.
    """
    text = llm_output.strip()

    # Attempt 1: direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Attempt 2: extract first JSON object from text
    match = re.search(r"\{[^}]+\}", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    # Fallback: treat entire response as a reply
    return {"action_type": "reply", "message": text}


# ═══════════════════════════════════════════════════════════════════════════
# Environment interaction
# ═══════════════════════════════════════════════════════════════════════════


def env_reset(task_level: Optional[str] = None) -> Dict[str, Any]:
    """Call /reset on the environment server."""
    payload = {}
    if task_level:
        payload["task_level"] = task_level
    resp = requests.post(f"{ENV_URL}/reset", json=payload)
    resp.raise_for_status()
    return resp.json()


def env_step(action: Dict[str, Any]) -> Dict[str, Any]:
    """Call /step on the environment server."""
    resp = requests.post(f"{ENV_URL}/step", json=action)
    resp.raise_for_status()
    return resp.json()


# ═══════════════════════════════════════════════════════════════════════════
# Agent loop
# ═══════════════════════════════════════════════════════════════════════════


def run_episode(task_level: str, max_steps: int = 8) -> Dict[str, Any]:
    """
    Run a single episode for the given task level.

    Returns the final observation (which contains the final_score in metadata).
    """
    obs = env_reset(task_level)
    history: List[str] = []
    accumulated_reward = 0.0

    # ── [START] log ───────────────────────────────────────────────────────
    log_start(
        task=task_level,
        ticket_id=obs["ticket_id"],
        customer_name=obs["customer_name"],
        customer_priority=obs["customer_priority"],
        goal=obs["goal"],
    )

    for step_num in range(1, max_steps + 1):
        if obs.get("done", False):
            break

        # Build prompt for the LLM
        prompt = (
            f"TICKET:\n{obs['ticket_text']}\n\n"
            f"CUSTOMER: {obs['customer_name']} | "
            f"Priority: {obs['customer_priority']}\n"
            f"STATUS: {obs['ticket_status']}\n"
            f"GOAL: {obs['goal']}\n\n"
            f"CONVERSATION SO FAR:\n"
        )
        for msg in obs.get("conversation_history", []):
            prompt += f"  [{msg.get('role', '?')}] {msg.get('content', '')}\n"
        if history:
            prompt += f"\nPREVIOUS ACTIONS & REWARDS:\n"
            for h in history:
                prompt += f"  {h}\n"
        prompt += "\nWhat is your next action? Return JSON only."

        # Call the LLM
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=300,
            )
            llm_text = response.choices[0].message.content or ""
        except Exception as e:
            print(f"  [LLM Error] {e}")
            llm_text = '{"action_type": "resolve"}'

        action = parse_action(llm_text)

        # Execute in the environment
        obs = env_step(action)
        reward = obs.get("reward", 0.0)
        accumulated_reward += reward
        history.append(f"Step {step_num}: {action['action_type']} → reward={reward}")

        # ── [STEP] log ───────────────────────────────────────────────────
        log_step(
            step=step_num,
            action=action,
            reward=reward,
            done=obs.get("done", False),
            ticket_status=obs["ticket_status"],
        )

    # ── [END] log ─────────────────────────────────────────────────────────
    final_score = obs.get("metadata", {}).get("final_score", 0.0)
    total_steps = step_num if obs.get("done", False) else max_steps

    log_end(
        task=task_level,
        ticket_id=obs.get("ticket_id", ""),
        final_score=float(final_score) if final_score else 0.0,
        total_steps=total_steps,
        accumulated_reward=accumulated_reward,
    )

    return obs


def main():
    """Run baseline inference across all three task levels."""
    print("=" * 60)
    print("  Customer Support Environment — Baseline Inference")
    print("=" * 60)
    print(f"  LLM: {MODEL_NAME} @ {API_BASE_URL}")
    print(f"  Env: {ENV_URL}")

    results = {}
    for level in ["easy", "medium", "hard"]:
        try:
            obs = run_episode(level)
            results[level] = obs.get("metadata", {}).get("final_score", 0.0)
        except Exception as e:
            print(f"  [Error in {level}] {e}")
            results[level] = 0.0

    # Summary
    print(f"\n{'='*60}")
    print("  RESULTS SUMMARY")
    print(f"{'='*60}")
    for level, score in results.items():
        bar = "#" * int(float(score or 0) * 20)
        print(f"  {level:8s}: {score}  {bar}")
    avg = sum(float(s or 0) for s in results.values()) / len(results)
    print(f"  {'average':8s}: {avg:.2f}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
