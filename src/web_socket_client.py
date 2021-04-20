import json
from abc import ABC, abstractmethod
from typing import Callable, Optional, Any

from websocket import WebSocketApp

from src.logger import AbstractLogger, Logger
from src.web_socket_message import WebSocketMessage


class AbstractWebSocketClient(ABC):
    @abstractmethod
    def register(self, on_open: Callable[[], None], on_message: Callable[[WebSocketMessage], None],
                 on_error: Callable[[Any], None], on_close: Callable[[], None]) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def send(self, web_socket_message: WebSocketMessage) -> None:
        pass


class WebSocketClient(AbstractWebSocketClient):
    __instance: Optional['WebSocketClient'] = None

    def __init__(self, logger: AbstractLogger = Logger()):
        if WebSocketClient.__instance:
            raise Exception('Use get_instance() instead!')
        self.__ws = WebSocketApp('wss://jqbx.fm/socket.io/?EIO=3&transport=websocket')
        self.__logger = logger
        WebSocketClient.__instance = self

    @staticmethod
    def get_instance() -> 'WebSocketClient':
        if WebSocketClient.__instance is None:
            WebSocketClient()
        return WebSocketClient.__instance

    def register(self, on_open: Callable[[], None], on_message: Callable[[WebSocketMessage], None],
                 on_error: Callable[[Any], None], on_close: Callable[[], None]) -> None:
        self.__ws.on_open = lambda _: on_open()
        self.__ws.on_message = lambda _, raw_message: on_message(self.__parse(raw_message))

    def run(self) -> None:
        self.__ws.run_forever()

    def send(self, web_socket_message: WebSocketMessage) -> None:
        self.__logger.info('Outgoing Message', web_socket_message.as_dict())
        serialized = str(web_socket_message.code)
        array_part = [x for x in [web_socket_message.label, web_socket_message.payload] if x]
        if array_part:
            serialized += json.dumps(array_part)
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
