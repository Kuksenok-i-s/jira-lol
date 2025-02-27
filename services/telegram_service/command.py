# telegram_service/commands.py

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from main_logic.scenarios.scenario_manager import ScenarioManager
from services.db_service.db_service import DBService

COMMANDS_INFO = {
    "start": "Запускает бота, приветственное сообщение",
    "help": "Показывает список доступных команд",
    "start_log": "Логирует время",
}

db = DBService("issues.db")

def register_commands(
        bot: AsyncTeleBot,
        scenario_manager: ScenarioManager = None,
) -> None:
    @bot.message_handler(commands=["start"])
    async def start_command(message: Message):
        db.save_chat_id(message.chat.id, "ololshka")
        text = "Привет! Я бот для логгирования часов в JIRA (пока в зачаточном состоянии). " "Для списка команд введите /help."
        await bot.send_message(message.chat.id, text)

    @bot.message_handler(commands=["help"])
    async def help_command(message: Message):
        help_text = "Список команд:\n\n"
        for cmd, desc in COMMANDS_INFO.items():
            help_text += f"/{cmd} - {desc}\n"
        await bot.send_message(message.chat.id, help_text)

    @bot.message_handler(commands=["start_log"])
    async def start_log_command(message: Message):
        user_id = message.from_user.id
        scenario = scenario_manager.start_log_time_scenario(user_id)
        await bot.send_message(message.chat.id, "Введите ключ задачи, в которую логируем.")
