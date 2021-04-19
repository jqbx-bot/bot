from abc import ABC, abstractmethod
from typing import Optional


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
    def process(self, user_id: str, payload: Optional[str]) -> None:
        pass
