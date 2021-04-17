from abc import ABC, abstractmethod


class AbstractBot(ABC):
    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def chat(self, message: str) -> None:
        pass
