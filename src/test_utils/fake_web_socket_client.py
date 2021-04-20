from typing import Callable, Optional, List, Any

from src.web_socket_client import AbstractWebSocketClient
from src.web_socket_message import WebSocketMessage


class FakeWebSocketClient(AbstractWebSocketClient):
    def __init__(self):
        self.__on_open: Optional[Callable[[], None]] = None
        self.__on_message: Optional[Callable[[WebSocketMessage], None]] = None
        self.__client_messages: List[WebSocketMessage] = []

    def register(self, on_open: Callable[[], None], on_message: Callable[[WebSocketMessage], None],
                 on_error: Callable[[Any], None] = None, on_close: Callable[[], None] = None) -> None:
        self.__on_open = on_open
        self.__on_message = on_message

    def run(self) -> None:
        self.__on_open()

    def send(self, web_socket_message: WebSocketMessage) -> None:
        self.__client_messages.append(web_socket_message)

    def send_server_message(self, web_socket_message: WebSocketMessage) -> None:
        self.__on_message(web_socket_message)

    def dequeue_client_messages(self) -> List[WebSocketMessage]:
        dequeued_client_messages = list(self.__client_messages)
        self.__client_messages = []
        return dequeued_client_messages
