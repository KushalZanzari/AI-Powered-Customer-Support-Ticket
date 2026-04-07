# 🚀 How to Run the Environment Locally

This guide will walk you through exactly how to get the AI Customer Support Environment running on your own laptop.

There are two ways to do this:
1. **The Python Way (Recommended for developers)**
2. **The Docker Way (Easiest if you have Docker installed)**

---

## 🛠️ Method 1: The Python Way

### Prerequisites
- Make sure you have **Python 3.10** (or newer) installed.
- Open your terminal (Mac/Linux) or Command Prompt/PowerShell (Windows).

### Step 1: Install Dependencies
Navigate to the project folder and install the required packages:

```bash
# Install the server dependencies
pip install -r env/server/requirements.txt

# Install the OpenAI library for the AI agent
pip install openai
```

### Step 2: Start the Environment Server
The environment runs as a local web server. Start it with this command:

```bash
python -m uvicorn env.server.app:app --host 0.0.0.0 --port 8000
```

You should see an output like this:
```text
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
**Leave this window open!** The server must stay running.

### Step 3: Run the AI Agent
Open a **new** terminal window. You need to set up your AI credentials before running the agent.

**If you are on Windows (Command Prompt / PowerShell):**
```cmd
set API_BASE_URL=https://api.openai.com/v1
set MODEL_NAME=gpt-4
set HF_TOKEN=your_actual_api_key_here
python inference.py
```

**If you are on Mac or Linux:**
```bash
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4"
export HF_TOKEN="your_actual_api_key_here"
python inference.py
```

The AI agent will now connect to the server, run through all 3 difficulty levels, and print its scores!

---

## 🐳 Method 2: The Docker Way

If you have Docker Desktop installed, you don't need to install Python packages manually. Docker handles everything.

### Step 1: Build the Docker Image
In your terminal, inside the project folder, run:

```bash
docker build -t customer-support-env -f env/server/Dockerfile .
```
*Note: Don't forget the `.` at the end of the command!*

### Step 2: Run the Docker Container
Once the build is finished, start the server with:

```bash
docker run -p 8000:8000 customer-support-env
```

### Step 3: Verify it is Running
Open your web browser and go to: `http://localhost:8000/health`
You should see: `{"status": "healthy", "environment": "customer-support-env"}`

Now, follow **Step 3 from Method 1** to run your `inference.py` script against the running Docker container!
