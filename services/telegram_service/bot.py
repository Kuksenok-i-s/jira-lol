# telegram_service/bot.py

import asyncio
from telebot.async_telebot import AsyncTeleBot

from services.config import Config
from .command import register_commands
from .handlers import register_handlers


class TelegramService:
    def __init__(self, config: Config):
        self.config = config
        self.bot = AsyncTeleBot(config.telegram_token)

    async def send_message(self, message: str) -> None:
        """
        Пример метода для отправки сообщений в нужный чат (ID берём из Config).
        """
        await self.bot.send_message(self.config.telegram_chat_id, message)

    def listen(self, utils, config, chatgpt, db) -> None:
        """
        Подключаем все команды и хендлеры, а затем запускаем polling.
        """
        register_commands(self.bot)
        register_handlers(self.bot)

        # Запуск асинхронного long-polling
        asyncio.run(self.bot.polling())
