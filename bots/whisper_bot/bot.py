import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from app.config import settings
import httpx

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command."""
    await update.message.reply_text("Whisper Bot started! Use /help for commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command."""
    await update.message.reply_text("Commands: /whisper message")

async def whisper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Whisper command."""
    message = " ".join(context.args) if context.args else "No message"
    # Register BPS event
    moderator_telegram_id = update.effective_user.id
    async with httpx.AsyncClient() as client:
        try:
            mod_resp = await client.get(f"http://localhost:8000/api/users/by_telegram/{moderator_telegram_id}")
            if mod_resp.status_code == 200:
                moderator_id = mod_resp.json()["id"]
                await client.post(f"http://localhost:8000/api/reputation/register_event", json={
                    "user_id": moderator_id,
                    "event_type": "message_sent",
                    "token": settings.core_secret
                })
        except:
            pass  # Ignore if fails
    await update.message.reply_text(f"Whisper: {message}")

def main():
    application = Application.builder().token(settings.telegram_whisper_bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("whisper", whisper))
    application.run_polling()

if __name__ == "__main__":
    main()