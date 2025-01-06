# telegram_service/scenarios/logtime_scenario.py

from .base_scenario import BaseScenario


class LogTimeScenario(BaseScenario):
    def __init__(self, user_id: int, jira_handler):
        super().__init__(user_id)
        self.jira_handler = jira_handler

        self.issue_key = None
        self.hours = None
        self.comment = None

    async def handle_message(self, bot, message):

        if self.issue_key is None:
            self.issue_key = message.text
            await bot.send_message(message.chat.id, "Сколько часов логгировать?")
            return

        if self.hours is None:
            self.hours = message.text
            await bot.send_message(message.chat.id, "Какой комментарий добавить?")
            return

        if self.comment is None:
            self.comment = message.text

            self.jira_handler.add_worklog(self.issue_key, f"{self.hours}h", self.comment)

            await bot.send_message(
                message.chat.id, f"Залогировал {self.hours}ч на задачу {self.issue_key} с комментарием '{self.comment}'."
            )

            self.current_step = 1  # ставим шаг в "завершён"
            return

    def is_finished(self) -> bool:
        return self.current_step == 1
