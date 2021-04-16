from abc import ABC, abstractmethod
from typing import Optional

from src.abstract_bot import AbstractBot
from src.bot_state import BotState


class AbstractCommandProcessor(ABC):
    @abstractmethod
    def process(self, bot: AbstractBot, state: BotState, payload: Optional[str]) -> None:
        pass
