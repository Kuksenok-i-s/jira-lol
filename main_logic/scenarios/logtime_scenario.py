# logtime_scenario.py

from services.jira_service.jira_service import JiraHandler
from telebot.async_telebot import types

from .base_scenario import BaseScenario


class LogTimeScenario(BaseScenario):  # Наследуем от BaseScenario
    def __init__(self, user_id: int, jira_handler: JiraHandler):
        super().__init__(user_id)
        self.jira_handler = jira_handler
        self.issue_key = None
        self.hours = None
        self.comment = None

    async def handle_message(self, bot, message: types.Message) -> None:
        if self.issue_key is None:
            self.issue_key = message.text
            await bot.send_message(message.chat.id, "Сколько часов логировать?")
            return

        if self.hours is None:
            self.hours = message.text
            await bot.send_message(message.chat.id, "Какой комментарий добавить?")
            return

        if self.comment is None:
            self.comment = message.text
            try:
                self.jira_handler.add_worklog(self.issue_key, f"{self.hours}h", self.comment)
                await bot.send_message(
                    message.chat.id,
                    f"Залогировал {self.hours}ч на задачу {self.issue_key} с комментарием '{self.comment}'."
                )
            except Exception as e:
                await bot.send_message(message.chat.id, f"Произошла ошибка при логировании времени: {str(e)}")

            self.current_step = 1
            return

    def is_finished(self) -> bool:
        return self.current_step == 1
