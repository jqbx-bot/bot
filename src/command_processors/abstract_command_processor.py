from abc import ABC, abstractmethod
from typing import Optional

from src.abstract_bot import AbstractBot


class AbstractCommandProcessor(ABC):
    @property
    @abstractmethod
    def keyword(self) -> str:
        pass

    @property
    @abstractmethod
    def help(self) -> str:
        pass

    @abstractmethod
    def process(self, bot: AbstractBot, user_id: str, payload: Optional[str]) -> None:
        pass
