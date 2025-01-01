# telegram_service/commands.py

from telebot.async_telebot import AsyncTeleBot

COMMANDS_INFO = {
    'start': 'Запускает бота, приветственное сообщение',
    'help': 'Показывает список доступных команд',
}


def register_commands(bot: AsyncTeleBot) -> None:

    @bot.message_handler(commands=['start'])
    async def start_command(message):
        text = (
            "Привет! Я бот для логгирования часов в JIRA (пока в зачаточном состоянии). "
            "Для списка команд введите /help."
        )
        await bot.send_message(message.chat.id, text)

    @bot.message_handler(commands=['help'])
    async def help_command(message):
        help_text = "Список команд:\n\n"
        for cmd, desc in COMMANDS_INFO.items():
            help_text += f"/{cmd} - {desc}\n"
        await bot.send_message(message.chat.id, help_text)