# telegram_service/handlers.py

from telebot.async_telebot import AsyncTeleBot

def register_handlers(bot: AsyncTeleBot) -> None:
    @bot.message_handler(func=lambda message: True)
    async def echo_message(message):
        await bot.reply_to(message, message.text)
