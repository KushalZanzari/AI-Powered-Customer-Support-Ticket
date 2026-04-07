@echo off
echo ==================================================
echo AI Customer Support Agent - Inference Runner
echo ==================================================

:: Replace the text below with your actual OpenAI API Key!
set HF_TOKEN=sk-your-real-key-goes-here

:: Set the other required variables
set API_BASE_URL=https://api.openai.com/v1
set MODEL_NAME=gpt-4o

:: Check if the key was updated
if "%HF_TOKEN%"=="sk-your-real-key-goes-here" (
    echo.
    echo ERROR: You need to add your real API key to this file first!
    echo Right-click 'run_agent.bat', choose 'Edit' or open it in Notepad,
    echo and replace 'sk-your-real-key-goes-here' with your real key.
    echo.
    pause
    exit /b
)

echo Starting the AI Agent...
echo.
python inference.py

echo.
pause
