
# 🎧 AI-Powered Customer Support Ticket Resolution Environment

> An OpenEnv-compatible simulation environment where AI agents learn to handle customer support tickets end-to-end — from reading queries, classifying issues, responding to customers, and escalating when needed.
[![OpenEnv](https://img.shields.io/badge/OpenEnv-compatible-blue)](https://github.com/meta-pytorch/OpenEnv)
[![Python](https://img.shields.io/badge/python-3.10+-green)](https://python.org)
[![Hugging Face](https://img.shields.io/badge/🤗_Live_on-Hugging_Face-blue)](https://kushalzanzari-ai-customer-support.hf.space/docs)


---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Architecture](#-architecture)
- [Environment Design](#-environment-design)
- [Tasks](#-tasks-easy--hard)
- [Quick Start](#-quick-start)
- [API Reference](#-api-reference)
- [Inference Script](#-inference-script)
- [Docker Deployment](#-docker-deployment)
- [Reward Design](#-reward-design)
- [Grading & Scoring](#-grading--scoring)
- [Project Structure](#-project-structure)

---

## 🎯 Problem Statement

Customer support automation is a high-impact real-world problem used by SaaS companies, e-commerce platforms, banks, and telecom providers. This environment provides a standardized benchmark for training and evaluating AI agents on realistic support workflows:

- **Reading** customer queries with varying complexity and tone
- **Classifying** issues into categories (billing, technical, account, general)
- **Taking actions** — reply, escalate, resolve, or request more information
- **Maintaining** conversation state across multi-step interactions

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────┐
│                  AI Agent (LLM)                     │
│        Reads observation → Decides action           │
└──────────────────────┬──────────────────────────────┘
                       │  HTTP (JSON)
                       ▼
┌─────────────────────────────────────────────────────┐
│              FastAPI Server (:8000)                 │
│  POST /reset  │  POST /step  │  GET /state          │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│            SupportEnvironment                       │
│  ┌─────────┐  ┌──────────┐  ┌──────────────────┐    │
│  │ Tickets │  │ Graders  │  │ Action Handlers  │    │
│  │ Database│  │(per task)│  │  classify/reply/ │    │
│  │ (16     │  │ easy     │  │  escalate/resolve│    │
│  │  cases) │  │ medium   │  │  request_info    │    │
│  │         │  │ hard     │  │                  │    │
│  └─────────┘  └──────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────┘
```

---

## 🎮 Environment Design

### Observation (State)

Each observation provides the agent with:

| Field | Type | Description |
|-------|------|-------------|
| `ticket_id` | string | Unique ticket identifier |
| `ticket_text` | string | The customer's message |
| `customer_name` | string | Customer name |
| `customer_priority` | string | `low` / `medium` / `high` / `critical` |
| `customer_history` | list | Previous interactions |
| `conversation_history` | list | Messages exchanged this episode |
| `ticket_status` | string | `open` / `classified` / `escalated` / `resolved` |
| `goal` | string | What the agent should accomplish |
| `current_task` | string | Difficulty level: `easy` / `medium` / `hard` |
| `done` | bool | Whether the episode has ended |
| `reward` | float | Step reward |
| `metadata` | dict | Additional info (errors, final score) |

### Action Space

| Action | Required Fields | Description |
|--------|----------------|-------------|
| `classify_issue` | `category` | Classify into: billing, technical, account, general |
| `reply` | `message` | Send a response to the customer |
| `escalate` | `team` | Escalate to: billing_team, technical_team, management, security_team |
| `resolve` | — | Mark the ticket as resolved |
| `request_more_info` | — | Ask the customer for more details |

---

## 📝 Tasks (Easy → Hard)

### Task 1: Easy — Basic FAQ Resolution

Simple, single-step queries (password reset, pricing info, data export).

- **Goal:** Classify → Reply with correct answer → Resolve
- **Example:** *"How do I reset my password?"*
- **Grading:** Keyword match + correct classification + resolution

### Task 2: Medium — Multi-step Issue Handling

Billing disputes, technical bugs, security concerns requiring investigation.

- **Goal:** Classify → Ask clarification → Provide solution → Resolve
- **Example:** *"I was charged twice for my subscription"*
- **Grading:** Sequence correctness + partial scoring

### Task 3: Hard — Complex Escalation Case

Angry customers with multiple issues, urgency, and emotional tone.

- **Goal:** Empathize → Classify → Escalate correctly → Resolve
- **Example:** *"I've been a loyal customer for 3 YEARS and your service is TERRIBLE..."*
- **Grading:** Empathy + urgency detection + correct escalation + resolution

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip

### Install & Run

```bash
# Clone the repository
git clone https://github.com/your-username/customer-support-env.git
cd customer-support-env

# Install dependencies
pip install -r env/server/requirements.txt

# Start the server
uvicorn env.server.app:app --host 0.0.0.0 --port 8000 --reload
```

### Test the API

```bash
# Reset with an easy task
curl -X POST http://localhost:8000/reset \
  -H "Content-Type: application/json" \
  -d '{"task_level": "easy"}'

# Classify the issue
curl -X POST http://localhost:8000/step \
  -H "Content-Type: application/json" \
  -d '{"action_type": "classify_issue", "category": "account"}'

# Reply to the customer
curl -X POST http://localhost:8000/step \
  -H "Content-Type: application/json" \
  -d '{"action_type": "reply", "message": "You can reset your password from the login page."}'

# Resolve the ticket
curl -X POST http://localhost:8000/step \
  -H "Content-Type: application/json" \
  -d '{"action_type": "resolve"}'
```

### Use the Python Client

```python
from env.client import SupportEnvClient

with SupportEnvClient("http://localhost:8000") as client:
    obs = client.reset(task_level="easy")
    print(f"Ticket: {obs['ticket_text']}")

    obs = client.step("classify_issue", category="account")
    obs = client.step("reply", message="Reset via Settings > Password.")
    obs = client.step("resolve")

    print(f"Final Score: {obs['metadata']['final_score']}")
```

---

## 📡 API Reference

### `POST /reset`

Start a new episode.

**Body (all optional):**
```json
{
  "task_level": "easy|medium|hard",
  "seed": 42,
  "episode_id": "my-episode-1"
}
```

### `POST /step`

Execute an action.

**Body:**
```json
{
  "action_type": "classify_issue",
  "category": "billing",
  "message": null,
  "team": null
}
```

### `GET /state`

Returns current episode state (step count, accumulated reward, flags).

### `GET /health`

Returns `{"status": "healthy"}`.

---

## 🤖 Inference Script

Run the baseline AI agent against all three task levels:

```bash
# Set your LLM credentials
export API_BASE_URL="https://api.openai.com/v1"
export API_KEY="sk-..."
export MODEL_NAME="gpt-4"

# Make sure the env server is running, then:
python inference.py
```

The script will run one episode per task level and print results:

```
══════════════════════════════════════════════════════════════
  RESULTS SUMMARY
══════════════════════════════════════════════════════════════
  easy    : 1.0   ████████████████████
  medium  : 0.75  ███████████████
  hard    : 0.6   ████████████
  average : 0.78
══════════════════════════════════════════════════════════════
```

---

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t customer-support-env -f env/server/Dockerfile .

# Run the container
docker run -p 8000:8000 customer-support-env

# Verify
curl http://localhost:8000/health
```

### Deploy to Hugging Face Spaces

1. Create a new HF Space (Docker type)
2. Push this repository
3. Tag with `openenv`
4. Verify: `curl -X POST https://your-space.hf.space/reset`

---

## 💰 Reward Design

| Outcome | Reward |
|---------|--------|
| Correct resolution | **+1.0** |
| Correct classification | **+0.5** |
| Helpful reply (≥2 keyword matches) | **+0.5** |
| Asked for clarification | **+0.3** |
| Partially helpful reply | **+0.2** |
| Correct escalation | **+0.5** |
| Wrong classification | **-0.2** |
| Bad / irrelevant reply | **-0.5** |
| Infinite loop (same action ×3) | **-1.0** |

---

## 📊 Grading & Scoring

Each task has a deterministic grader returning a score from **0.0 to 1.0**:

### Easy Grader
| Component | Weight |
|-----------|--------|
| Correct classification | 0.3 |
| Helpful reply | 0.4 |
| Resolved | 0.3 |

### Medium Grader
| Component | Weight |
|-----------|--------|
| Correct classification | 0.25 |
| Asked clarification | 0.25 |
| Correct solution | 0.30 |
| Resolved | 0.20 |

### Hard Grader
| Component | Weight |
|-----------|--------|
| Empathetic response | 0.20 |
| Urgency detected | 0.20 |
| Correct classification | 0.20 |
| Correct escalation team | 0.20 |
| Resolved / escalated | 0.20 |

---

## 📁 Project Structure

```
├── env/
│   ├── __init__.py              # Package exports
│   ├── models.py                # Action, Observation, State dataclasses
│   ├── client.py                # HTTP client for the environment
│   ├── graders.py               # Deterministic scoring functions
│   ├── ticket_data.py           # 16 curated ticket scenarios
│   ├── openenv.yaml             # OpenEnv manifest
│   ├── pyproject.toml           # Package configuration
│   └── server/
│       ├── __init__.py
│       ├── support_environment.py  # Core environment logic
│       ├── app.py               # FastAPI application
│       ├── requirements.txt     # Server dependencies
│       └── Dockerfile           # Container image
├── inference.py                 # Baseline LLM agent script
├── validate_submission.sh       # Submission validation
├── README.md                    # This file
└── .gitignore
```
---
title: AI Customer Support
emoji: 🎧
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
tags:
  - openenv
---





