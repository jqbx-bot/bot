from abc import ABC, abstractmethod
from typing import List, Optional


class AbstractBot(ABC):
    @property
    @abstractmethod
    def mod_ids(self) -> List[str]:
        pass

    @property
    @abstractmethod
    def welcome_message(self) -> Optional[str]:
        pass

    @abstractmethod
    def set_welcome_message(self, welcome_message: Optional[str]) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def chat(self, message: str, recipients: Optional[List[dict]] = None) -> None:
        pass
