import logging

from aiogram import BaseMiddleware
from aiogram.types import Message


class LoggingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.logger = logging.getLogger('aiogram.contrib.middleware.logging')

    async def __call__(self, handler, event: Message, data):
        self.logger.info(f"[DEBUG] {event.from_user.id} | {event.text}")
        return await handler(event, data)