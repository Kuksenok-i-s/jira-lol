import asyncio

from services.config import Config

from telebot.async_telebot import AsyncTeleBot


class TelegramService:
    def __init__(self, config: Config):
        self.config = config
        self.bot = AsyncTeleBot(config.telegram_token)

    async def send_message(self, message):
        await self.bot.send_message(self.config.telegram_chat_id, message)

    def listen(self, utils, config, chatgpt, db):
        @self.bot.message_handler(commands=['help', 'start'])
        async def send_welcome(message):
            text = 'Hi, I am EchoBot.\nJust write me something and I will repeat it!'
            await self.bot.reply_to(message, text)

        @self.bot.message_handler(func=lambda message: True)
        async def echo_message(message):
            await self.bot.reply_to(message, message.text)

        asyncio.run(self.bot.polling())