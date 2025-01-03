# telegram_service/scenarios/base_scenario.py

class BaseScenario:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.current_step = 0

    async def handle_message(self, bot, message):
        raise NotImplementedError

    def is_finished(self) -> bool:
        return False
