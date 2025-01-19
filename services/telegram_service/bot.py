# bot.py

import asyncio
from telebot.async_telebot import AsyncTeleBot
from config import Config
from .command import register_commands
from .handlers import register_handlers
from main_logic import ScenarioManager
from services.jira_service.jira_service import JiraHandler, JiraService

from telebot.types import BotCommand

class TelegramService:
    def __init__(self, config: Config):
        self.config = config
        self.bot = AsyncTeleBot(config.telegram_token)

        self.jira_service = JiraService(url=config.jira_url, user=config.jira_user, token=config.jira_token)
        self.jira_handler = JiraHandler(js=self.jira_service, config=config, git_summary={})

        self.scenario_manager = ScenarioManager(self.jira_handler)

    async def set_commands(self):
        commands = [
            BotCommand(command="start", description="Запускает бота, приветственное сообщение"),
            BotCommand(command="help", description="Показывает список доступных команд"),
            BotCommand(command="start_log", description="Логирует время"),
        ]
        await self.bot.set_my_commands(commands)

    async def send_message(self, chat_id: int, message: str) -> None:
        await self.bot.send_message(chat_id, message)

    def listen(self, utils, config, chatgpt, db) -> None:
        register_commands(self.bot, self.scenario_manager)
        register_handlers(self.bot, self.scenario_manager)

        asyncio.run(self.start_bot())

    async def start_bot(self):
        await self.set_commands()
        await self.bot.polling()
