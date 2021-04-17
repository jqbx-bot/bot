import json
from abc import ABC, abstractmethod
from typing import Callable

from websocket import WebSocketApp

from src.web_socket_message import WebSocketMessage


class AbstractWebSocketClient(ABC):
    @abstractmethod
    def register(self, on_open=Callable[[], None], on_message=Callable[[WebSocketMessage], None]) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def send(self, web_socket_message: WebSocketMessage) -> None:
        pass


class WebSocketClient(AbstractWebSocketClient):
    def __init__(self):
        self.__ws = WebSocketApp('wss://jqbx.fm/socket.io/?EIO=3&transport=websocket')

    def register(self, on_open=Callable[[], None], on_message=Callable[[WebSocketMessage], None]) -> None:
        self.__ws.on_open = lambda _: on_open()
        self.__ws.on_message = lambda _, raw_message: on_message(self.__parse(raw_message))

    def run(self) -> None:
        self.__ws.run_forever()

    def send(self, web_socket_message: WebSocketMessage) -> None:
        serialized = '%s["%s"' % (web_socket_message.code, web_socket_message.label)
        if web_socket_message.payload is not None:
            serialized += ',%s' % json.dumps(web_socket_message.payload)
        serialized += ']'
        self.__ws.send(serialized)

    @staticmethod
    def __parse(raw_message: str) -> WebSocketMessage:
        stripped = raw_message.strip()
        parts = stripped.split('[', 1)
        label = None
        payload = None
        if len(parts) > 1:
            json_array = json.loads('[%s' % parts[1])
            label = json_array[0]
            payload = None if len(json_array) == 1 else json_array[1]
        return WebSocketMessage(int(parts[0]), label, payload)
