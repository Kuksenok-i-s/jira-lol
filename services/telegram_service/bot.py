# telegram_service/bot.py

import asyncio
from telebot.async_telebot import AsyncTeleBot

from config import Config

from .command import register_commands
from .handlers import register_handlers

from main_logic import ScenarioManager
from services.jira_service.jira_service import JiraHandler, JiraService


class TelegramService:
    def __init__(self, config: Config):
        self.config = config
        self.bot = AsyncTeleBot(config.telegram_token)

        self.jira_service = JiraService(url=config.jira_url, user=config.jira_user, token=config.jira_token)
        self.jira_handler = JiraHandler(js=self.jira_service, config=config, git_summary={})

        self.scenario_manager = ScenarioManager(self.jira_handler)

    async def send_message(self, message: str) -> None:
        await self.bot.send_message(self.config.telegram_chat_id, message)

    def listen(self, utils, config, chatgpt, db) -> None:
        register_commands(self.bot, self.scenario_manager)
        register_handlers(self.bot, self.scenario_manager)

        asyncio.run(self.bot.polling())
