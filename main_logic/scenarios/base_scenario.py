# telegram_service/scenarios/base_scenario.py
from abc import ABC, abstractmethod


class BaseScenario(ABC):
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.current_step = 0

    @abstractmethod
    async def handle_message(self, bot, message): ...

    @abstractmethod
    def is_finished(self) -> bool: ...
