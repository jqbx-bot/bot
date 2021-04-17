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

    @property
    @abstractmethod
    def current_track(self) -> Optional[dict]:
        pass

    @property
    @abstractmethod
    def doped(self) -> bool:
        pass

    @property
    @abstractmethod
    def noped(self) -> bool:
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

    @abstractmethod
    def dope(self) -> None:
        pass

    @abstractmethod
    def nope(self) -> None:
        pass
