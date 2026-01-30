@echo off
echo Starting Hasbullita MVP Bot...

REM Check if .env exists
if not exist .env (
    echo Error: .env file not found. Copy .env.example to .env and configure TELEGRAM_BOT_TOKEN
    pause
    exit /b 1
)

REM Install dependencies if needed
pip install -r requirements.txt

REM Run the bot
python app/main.py