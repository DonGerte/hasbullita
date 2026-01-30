import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from app.config import settings
import httpx

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command."""
    await update.message.reply_text("Admin Bot started! Use /help for commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command."""
    await update.message.reply_text("Commands: /ban @user reason, /mute @user reason")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban a user."""
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Usage: /ban @user reason")
        return
    user_mention = context.args[0]
    reason = " ".join(context.args[1:])
    # Assume user_mention is @username, but for simplicity, assume it's telegram_id
    # In real, need to resolve username to id, but for demo, assume user_mention is telegram_id
    try:
        user_telegram_id = int(user_mention.lstrip('@'))
    except ValueError:
        await update.message.reply_text("Invalid user")
        return
    group_id = str(update.effective_chat.id)
    moderator_telegram_id = update.effective_user.id
    # Get user_id from core
    async with httpx.AsyncClient() as client:
        try:
            user_resp = await client.get(f"http://localhost:8000/api/users/by_telegram/{user_telegram_id}")
            if user_resp.status_code != 200:
                await update.message.reply_text("User not found in core")
                return
            user_id = user_resp.json()["id"]
            mod_resp = await client.get(f"http://localhost:8000/api/users/by_telegram/{moderator_telegram_id}")
            if mod_resp.status_code != 200:
                await update.message.reply_text("Moderator not found")
                return
            moderator_id = mod_resp.json()["id"]
            ban_resp = await client.post(f"http://localhost:8000/api/moderation/ban", json={
                "user_id": user_id,
                "group_id": group_id,
                "reason": reason,
                "moderator_id": moderator_id,
                "token": settings.core_secret
            })
            if ban_resp.status_code == 200:
                await update.message.reply_text("User banned")
                # Register BPS event
                await client.post(f"http://localhost:8000/api/reputation/register_event", json={
                    "user_id": moderator_id,
                    "event_type": "message_sent",
                    "token": settings.core_secret
                })
            else:
                await update.message.reply_text("Error banning user")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mute a user."""
    # Similar to ban
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Usage: /mute @user reason")
        return
    user_mention = context.args[0]
    reason = " ".join(context.args[1:])
    try:
        user_telegram_id = int(user_mention.lstrip('@'))
    except ValueError:
        await update.message.reply_text("Invalid user")
        return
    group_id = str(update.effective_chat.id)
    moderator_telegram_id = update.effective_user.id
    async with httpx.AsyncClient() as client:
        try:
            user_resp = await client.get(f"http://localhost:8000/api/users/by_telegram/{user_telegram_id}")
            if user_resp.status_code != 200:
                await update.message.reply_text("User not found")
                return
            user_id = user_resp.json()["id"]
            mod_resp = await client.get(f"http://localhost:8000/api/users/by_telegram/{moderator_telegram_id}")
            if mod_resp.status_code != 200:
                await update.message.reply_text("Moderator not found")
                return
            moderator_id = mod_resp.json()["id"]
            mute_resp = await client.post(f"http://localhost:8000/api/moderation/mute", json={
                "user_id": user_id,
                "group_id": group_id,
                "reason": reason,
                "moderator_id": moderator_id,
                "token": settings.core_secret
            })
            if mute_resp.status_code == 200:
                await update.message.reply_text("User muted")
                # Register BPS event
                await client.post(f"http://localhost:8000/api/reputation/register_event", json={
                    "user_id": moderator_id,
                    "event_type": "message_sent",
                    "token": settings.core_secret
                })
            else:
                await update.message.reply_text("Error muting user")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

def main():
    application = Application.builder().token(settings.telegram_admin_bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ban", ban))
    application.add_handler(CommandHandler("mute", mute))
    application.run_polling()

if __name__ == "__main__":
    main()