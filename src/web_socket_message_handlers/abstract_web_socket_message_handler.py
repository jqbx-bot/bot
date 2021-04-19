from abc import ABC, abstractmethod

from src.web_socket_message import WebSocketMessage


class AbstractWebSocketMessageHandler(ABC):
    @property
    @abstractmethod
    def message_label(self) -> str:
        pass

    @abstractmethod
    def handle(self, message: WebSocketMessage) -> None:
        pass
