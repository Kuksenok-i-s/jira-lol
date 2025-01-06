# telegram_service/scenarios/scenario_manager.py

from .logtime_scenario import LogTimeScenario


class ScenarioManager:
    def __init__(self, jira_handler):
        self.jira_handler = jira_handler
        self.active_scenarios = {}

    def start_log_time_scenario(self, user_id: int) -> LogTimeScenario:
        scenario = LogTimeScenario(user_id, self.jira_handler)
        self.active_scenarios[user_id] = scenario
        return scenario

    async def handle_message(self, bot, message) -> bool:
        user_id = message.from_user.id
        scenario = self.active_scenarios.get(user_id)

        if scenario:
            await scenario.handle_message(bot, message)
            if scenario.is_finished():
                del self.active_scenarios[user_id]
            return True

        return False
