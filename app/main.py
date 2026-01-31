import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import types
from aiogram.filters import Command
from app.config import settings as config
from app.storage.repository import init_db
from app.bot.handlers.start import start_handler
from app.bot.handlers.message import message_handler
from app.bot.handlers.commands import help_handler, stats_handler, suggest_handler, mood_handler, quiz_handler, achievements_handler, info_handler, callback_handler, inspire_handler, weather_handler, moon_handler, news_handler, horoscope_handler, meme_handler
from app.bot.middlewares.error_logging import ErrorLoggingMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    # Initialize database
    init_db()
    logger.info("Database initialized")

    # Initialize bot
    bot = Bot(token=config.telegram_bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Add middleware
    dp.message.middleware.register(ErrorLoggingMiddleware())

    # Register handlers
    dp.message.register(start_handler, Command("start"))
    dp.message.register(help_handler, Command("help"))
    dp.message.register(info_handler, Command("info"))
    dp.message.register(stats_handler, Command("stats"))
    dp.message.register(suggest_handler, Command("suggest"))
    dp.message.register(mood_handler, Command("mood"))
    dp.message.register(quiz_handler, Command("quiz"))
    dp.message.register(achievements_handler, Command("achievements"))
    dp.message.register(inspire_handler, Command("inspire"))
    dp.message.register(weather_handler, Command("weather"))
    dp.message.register(moon_handler, Command("moon"))
    dp.message.register(news_handler, Command("news"))
    dp.message.register(horoscope_handler, Command("horoscope"))
    dp.message.register(meme_handler, Command("meme"))
    dp.message.register(message_handler)

    # Register callback handler
    dp.callback_query.register(callback_handler)

    # Start polling
    logger.info("Bot started")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
