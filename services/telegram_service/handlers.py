# telegram_service/handlers.py

from telebot.async_telebot import AsyncTeleBot

def register_handlers(bot: AsyncTeleBot, scenario_manager):
    @bot.message_handler(func=lambda message: True)
    async def default_handler(message):
        handled = await scenario_manager.handle_message(bot, message)
        if not handled:
            await bot.reply_to(message, message.text)
