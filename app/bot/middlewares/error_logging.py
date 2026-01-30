from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from app.core.metrics import log_error

class ErrorLoggingMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        try:
            await self.handler(message, data)
        except Exception as e:
            log_error(str(e))
            # Re-raise to let aiogram handle it
            raise