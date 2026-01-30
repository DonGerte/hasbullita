import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.core.config import config
from app.storage.repository import init_db
from app.bot.handlers.start import start_handler
from app.bot.handlers.message import message_handler
from app.bot.middlewares.error_logging import ErrorLoggingMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Initialize database
    init_db()
    logger.info("Database initialized")

    # Initialize bot
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Add middleware
    dp.middleware.setup(ErrorLoggingMiddleware())

    # Register handlers
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(message_handler, content_types=types.ContentTypes.TEXT)

    # Start polling
    logger.info("Bot started")
    try:
        await dp.start_polling()
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())