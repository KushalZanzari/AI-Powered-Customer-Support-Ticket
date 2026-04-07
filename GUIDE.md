# 🎧 AI Customer Support Agent — Beginner's Guide

> **In simple words:** This project creates a practice ground where AI learns how to handle customer support messages — just like a new employee practices handling complaints before talking to real customers.

---

## 🤔 What Is This Project?

Imagine you just joined a company as a customer support agent. Before you start talking to real customers, your manager gives you **practice tickets** — some easy, some tricky, and some really tough ones with angry customers. You practice on these, get feedback on your answers, and slowly get better.

**This project does the same thing — but for AI.**

We built a virtual "training room" where an AI agent receives customer support tickets and learns to:

- 📖 **Read** what the customer is asking
- 🏷️ **Classify** the problem (Is it a billing issue? A technical bug? An account question?)
- 💬 **Reply** with a helpful answer
- 🚨 **Escalate** serious problems to the right team (managers, security, etc.)
- ✅ **Resolve** the ticket when the customer is satisfied

The AI gets a **score** after each practice session — like a test grade — so we can measure how good it is.

---

## 🧐 Why Was This Made?

### The Real-World Problem

Every company gets customer support messages. Handling them well is important:
- Customers want **fast, accurate** answers
- Companies spend **millions of dollars** on support teams
- Bad support = **unhappy customers who leave**

### The Solution

Instead of building a separate AI for each company, we built a **standardized training ground** (called an "environment") where:

1. **Researchers** can train AI agents to handle support tickets
2. **Companies** can test how well an AI would perform before using it
3. **Developers** can compare different AI models on the same tasks

Think of it like a **driving test** — we created the test track and the scoring system. Anyone can bring their AI "driver" and see how well it performs.

---

## 🎮 How Does It Work?

### The Simple Version

```
Customer sends a message  →  AI reads it  →  AI takes action  →  AI gets a score
```

### The Detailed Version

The system works in a loop called an **episode** (one complete ticket from start to finish):

```
┌──────────────────────────────────────────────┐
│          🤖 AI Agent (the student)           |
│                                              │
│   Reads the ticket → Decides what to do      │
└──────────────────┬───────────────────────────┘
                   │  sends action
                   ▼
┌──────────────────────────────────────────────┐
│      🏢 Our Environment (the teacher)        │
│                                              │
│   Checks the action → Gives a score          │
│   Sends back updated info                    │
└──────────────────────────────────────────────┘
```

**Step by step:**

1. **Reset** — The AI says "give me a new ticket to practice on"
2. **Read** — The AI reads the customer's message, name, priority level, etc.
3. **Act** — The AI picks one of 5 possible actions (explained below)
4. **Score** — Our system checks the action and gives a score (good or bad)
5. **Repeat** steps 2–4 until the ticket is resolved
6. **Final Grade** — A number from 0.0 (terrible) to 1.0 (perfect)

---

## 🎯 The 5 Actions an AI Can Take

Think of these as the 5 "moves" in the AI's toolbox:

| # | Action | What It Does | Real-Life Example |
|---|--------|-------------|-------------------|
| 1 | **Classify Issue** | Labels the type of problem | "This is a *billing* issue" |
| 2 | **Reply** | Sends a helpful message to the customer | "You can reset your password from Settings" |
| 3 | **Escalate** | Passes the ticket to a specialist team | "Sending this to the *management* team" |
| 4 | **Request More Info** | Asks the customer for more details | "Can you share your transaction ID?" |
| 5 | **Resolve** | Marks the ticket as done | "This ticket is now closed" |

---

## 📝 The 3 Difficulty Levels

We created **3 levels** of practice tickets, just like a video game:

### 🟢 Level 1: Easy — Basic Questions

Simple questions with clear answers. Think of it like a customer asking "Where is the bathroom?"

> **Example ticket:** *"How do I reset my password?"*
>
> **What AI should do:** Classify → Reply with instructions → Resolve
>
> **How we grade:** Did it classify correctly? Was the reply helpful? Did it resolve?

### 🟡 Level 2: Medium — Tricky Problems

Problems that need investigation and follow-up questions. Like a customer saying "I was charged the wrong amount."

> **Example ticket:** *"I was charged twice for my subscription!"*
>
> **What AI should do:** Classify → Ask for details → Provide a solution → Resolve
>
> **How we grade:** Correct classification + asked for info + good solution + resolved

### 🔴 Level 3: Hard — Angry Customers with Big Problems

Frustrated customers with multiple issues and emotional language. The toughest test.

> **Example ticket:** *"I've been a customer for 3 YEARS and your service is TERRIBLE! My data was LOST and I was overcharged!"*
>
> **What AI should do:** Respond with empathy first → Classify → Escalate to managers → Resolve
>
> **How we grade:** Was it empathetic? Detected urgency? Right classification? Right team? Resolved?

---

## 📊 How Scoring Works

### Per-Action Rewards

Every action the AI takes gets a **reward** (positive = good, negative = bad):

| What the AI Did | Score |
|-----------------|-------|
| ✅ Classified the issue correctly | **+0.5** |
| ✅ Sent a helpful reply (matched keywords) | **+0.5** |
| ✅ Resolved the ticket | **+1.0** |
| ✅ Asked for more info (when needed) | **+0.3** |
| ✅ Escalated to the correct team | **+0.5** |
| ❌ Classified the issue wrong | **-0.2** |
| ❌ Sent an unhelpful reply | **-0.5** |
| ❌ Repeated the same action 3 times in a row | **-1.0** |

### Final Grade

At the end of each ticket, a **final grade** is calculated from **0.0** (worst) to **1.0** (perfect).

The grading is **deterministic** — meaning the same actions will always get the same score. No randomness, no unfairness.

### Grade Breakdown by Level

**🟢 Easy — 3 things are checked:**

| What We Check | How Much It Counts |
|---------------|-------------------|
| Correct classification | 30% of the grade |
| Helpful reply | 40% of the grade |
| Ticket resolved | 30% of the grade |

**🟡 Medium — 4 things are checked:**

| What We Check | How Much It Counts |
|---------------|-------------------|
| Correct classification | 25% of the grade |
| Asked for clarification | 25% of the grade |
| Correct solution | 30% of the grade |
| Ticket resolved | 20% of the grade |

**🔴 Hard — 5 things are checked:**

| What We Check | How Much It Counts |
|---------------|-------------------|
| Empathetic response | 20% of the grade |
| Urgency detected | 20% of the grade |
| Correct classification | 20% of the grade |
| Correct escalation team | 20% of the grade |
| Resolved / escalated | 20% of the grade |

---

## 🚀 How to Set Up & Run (Step by Step)

### What You Need First

- **Python 3.10 or newer** — [Download here](https://python.org/downloads). Python is a programming language. Think of it as the "engine" that makes this project run.
- **pip** — Comes automatically with Python. It's a tool to install extra software packages.
- **A terminal/command prompt** — Where you type commands. On Windows, press `Win + R`, type `cmd`, and press Enter.

### Step 1: Get the Code

```bash
git clone https://github.com/your-username/customer-support-env.git
cd customer-support-env
```

> 💡 **What does this do?** Downloads the project files to your computer and enters the project folder.

### Step 2: Install Required Packages

```bash
pip install -r env/server/requirements.txt
pip install openai
```

> 💡 **What does this do?** Installs all the extra tools (like FastAPI and OpenAI) that this project needs to work.

### Step 3: Start the Server

```bash
uvicorn env.server.app:app --host 0.0.0.0 --port 8000
```

You should see something like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

> 💡 **What does this do?** Starts the "training room" — the environment is now running and waiting for the AI agent to connect.

**Keep this terminal open!** The server needs to stay running.

### Step 4: Run the AI Agent

Open a **new terminal window** (don't close the server!) and run:

**On Mac/Linux:**
```bash
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4"
export HF_TOKEN="your-api-key-here"
python inference.py
```

**On Windows (Command Prompt):**
```cmd
set API_BASE_URL=https://api.openai.com/v1
set MODEL_NAME=gpt-4
set HF_TOKEN=your-api-key-here
python inference.py
```

> 💡 **What does this do?** Tells the AI which model to use and gives it a key to access the AI service, then runs the agent.

### What You'll See

The AI will practice on all 3 levels and print its scores:

```
[START] {"task": "easy", "ticket_id": "EASY-001", ...}
[STEP]  {"step": 1, "action": {"action_type": "classify_issue"}, "reward": 0.5, ...}
[STEP]  {"step": 2, "action": {"action_type": "reply"}, "reward": 0.5, ...}
[STEP]  {"step": 3, "action": {"action_type": "resolve"}, "reward": 1.0, ...}
[END]   {"task": "easy", "final_score": 1.0, ...}

  RESULTS SUMMARY
  easy    : 1.0   ████████████████████
  medium  : 0.75  ███████████████
  hard    : 0.6   ████████████
  average : 0.78
```

---

## 🐳 Running with Docker (The Easy Way)

**What is Docker?** Docker packages everything (code + tools + settings) into a single "box" called a container. You don't need to install Python packages separately.

```bash
# Build the box
docker build -t customer-support-env -f env/server/Dockerfile .

# Run it
docker run -p 8000:8000 customer-support-env

# Check if it's working (in another terminal)
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```

---

## 🌐 Deploying Online (Hugging Face Spaces)

Want to run this on the internet so anyone can use it? Hugging Face Spaces lets you do that for free:

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and create a new Space
2. Choose **Docker** as the type
3. Push this code to the Space
4. Tag the Space with `openenv`
5. Wait for it to deploy (takes a few minutes)
6. Test it: visit `https://your-space.hf.space/health`

---

## 📡 The 4 Endpoints (How the AI Talks to the Environment)

The environment runs as a web server. The AI communicates with it using web requests (like clicking links, but for machines). Here are the 4 "doors" the AI can knock on:

### 🟢 `/health` — "Are you there?"
```
GET http://localhost:8000/health
→ {"status": "healthy"}
```

### 🔵 `/reset` — "Give me a new ticket"
```
POST http://localhost:8000/reset
Send: {"task_level": "easy"}
→ Gets back: ticket text, customer name, priority, goal, etc.
```

### 🟡 `/step` — "Here's my action"
```
POST http://localhost:8000/step
Send: {"action_type": "classify_issue", "category": "billing"}
→ Gets back: reward, updated status, whether ticket is done, etc.
```

### 🟣 `/state` — "What's the current situation?"
```
GET http://localhost:8000/state
→ Gets back: step count, accumulated reward, flags, etc.
```

---

## 🔧 Using the Python Helper (Easiest Way to Try)

If you don't want to deal with web requests, we provide a simple Python helper:

```python
from env.client import SupportEnvClient

# Connect to the server
client = SupportEnvClient("http://localhost:8000")

# Get a new easy ticket
obs = client.reset(task_level="easy")
print(f"Customer says: {obs['ticket_text']}")

# Step 1: Classify the issue
obs = client.step("classify_issue", category="account")
print(f"Reward: {obs['reward']}")

# Step 2: Reply to the customer
obs = client.step("reply", message="You can reset your password from Settings.")
print(f"Reward: {obs['reward']}")

# Step 3: Mark as done
obs = client.step("resolve")
print(f"Final Score: {obs['metadata']['final_score']}")

client.close()
```

---

## 📁 What Each File Does

```
📂 customer-support-env/
│
├── 📄 inference.py              ← The AI agent script (runs the AI against the environment)
├── 📄 test_e2e.py               ← Tests to make sure everything works correctly
├── 📄 validate_submission.sh    ← Checker script to run before submission
├── 📄 README.md                 ← Technical documentation
├── 📄 GUIDE.md                  ← This file (beginner-friendly guide)
│
└── 📂 env/                      ← The environment package (the "training room")
    ├── 📄 __init__.py            ← Package setup file
    ├── 📄 models.py              ← Defines what actions, observations, and rewards look like
    ├── 📄 client.py              ← Easy-to-use Python helper for talking to the server
    ├── 📄 graders.py             ← The "teacher" — scores the AI's performance
    ├── 📄 ticket_data.py         ← 16 realistic customer support scenarios (the "test questions")
    ├── 📄 openenv.yaml           ← Metadata about this environment
    ├── 📄 pyproject.toml         ← Python package settings
    │
    └── 📂 server/                ← The web server (listens for AI requests)
        ├── 📄 app.py             ← The 4 endpoints (reset, step, state, health)
        ├── 📄 support_environment.py ← Core game logic (handles actions, calculates rewards)
        ├── 📄 requirements.txt   ← List of required Python packages
        └── 📄 Dockerfile         ← Instructions to build a Docker container
```

---

## ❓ Frequently Asked Questions

### Q: Do I need to pay anything to run this?
**A:** The environment itself is free. However, if you want to use an AI model like GPT-4, you need an API key from OpenAI (which has costs per use). You can also use free/open-source models.

### Q: Can I add my own customer support tickets?
**A:** Yes! Open `env/ticket_data.py` and add new ticket dictionaries following the same format as the existing ones.

### Q: What if I don't have Docker?
**A:** Docker is optional. You can run the project directly with Python (Steps 1–4 in the setup section).

### Q: How do I know if my AI is doing well?
**A:** Look at the final scores. Anything above **0.7 average** across all 3 levels is good. Getting **1.0** on all levels means the AI handled everything perfectly.

### Q: Can I use a different AI model instead of GPT-4?
**A:** Yes! Change the `MODEL_NAME` and `API_BASE_URL` environment variables. Any model that supports the OpenAI API format will work (like Llama, Mistral, Claude, etc.).

---

## 📊 Quick Reference — Environment Variables

| Variable | What It Is | Required? | Example |
|----------|-----------|-----------|---------|
| `API_BASE_URL` | Where the AI model lives (its web address) | Yes | `https://api.openai.com/v1` |
| `MODEL_NAME` | Which AI model to use | Yes | `gpt-4` |
| `HF_TOKEN` | Your API key / access token | Yes | `sk-abc123...` |
| `ENV_URL` | Where the environment server is running | No (default: `http://localhost:8000`) | `http://localhost:8000` |

---

## 📄 License

BSD-3-Clause — You are free to use, modify, and share this project.

---

*Built with ❤️ for the [OpenEnv](https://github.com/meta-pytorch/OpenEnv) ecosystem.*
