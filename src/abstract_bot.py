from abc import ABC, abstractmethod

from src.message import Message


class AbstractBot(ABC):
    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def send(self, message: Message) -> None:
        pass

    @abstractmethod
    def chat(self, message: str) -> None:
        pass