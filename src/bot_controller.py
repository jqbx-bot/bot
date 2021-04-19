from abc import ABC, abstractmethod
from typing import List, Optional, Union

from src.env import AbstractEnvironment, Environment
from src.helpers import get_bot_user
from src.web_socket_client import AbstractWebSocketClient, WebSocketClient
from src.web_socket_message import WebSocketMessage


class AbstractBotController(ABC):
    @abstractmethod
    def chat(self, message: Union[str, List[str]]) -> None:
        pass

    @abstractmethod
    def whisper(self, message: str, recipient: dict) -> None:
        pass

    @abstractmethod
    def dope(self) -> None:
        pass

    @abstractmethod
    def nope(self) -> None:
        pass

    @property
    @abstractmethod
    def welcome_message(self) -> Optional[str]:
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
    def reset_vote(self) -> None:
        pass


class BotController(AbstractBotController):
    __instance: Optional['BotController'] = None

    def __init__(self, env: AbstractEnvironment = Environment(),
                 web_socket_client: AbstractWebSocketClient = WebSocketClient.get_instance()):
        if BotController.__instance:
            raise Exception('Use get_instance() instead!')
        self.__env = env
        self.__web_socket_client = web_socket_client
        self.__welcome_message: Optional[str] = None
        self.__current_track: Optional[dict] = None
        self.__doped: bool = False
        self.__noped: bool = False
        BotController.__instance = self

    @staticmethod
    def get_instance() -> 'BotController':
        if BotController.__instance is None:
            BotController()
        return BotController.__instance

    def chat(self, message: Union[str, List[str]]) -> None:
        messages = message if isinstance(message, list) else [message]
        for msg in messages:
            payload = {
                'roomId': self.__env.get_jqbx_room_id(),
                'user': get_bot_user(self.__env),
                'message': {
                    'message': msg,
                    'user': get_bot_user(self.__env),
                    'selectingEmoji': False
                }
            }
            self.__web_socket_client.send(WebSocketMessage(label='chat', payload=payload))

    def whisper(self, message: str, recipient: dict) -> None:
        payload = {
            'roomId': self.__env.get_jqbx_room_id(),
            'user': get_bot_user(self.__env),
            'message': {
                'message': '@%s %s' % (recipient['username'], message),
                'user': get_bot_user(self.__env),
                'recipients': [recipient],
                'selectingEmoji': False
            }
        }
        self.__web_socket_client.send(WebSocketMessage(label='chat', payload=payload))

    def dope(self) -> None:
        if self.__doped or self.__noped:
            return
        self.__web_socket_client.send(WebSocketMessage(label='thumbsUp', payload={
            'roomId': self.__env.get_jqbx_room_id(),
            'user': get_bot_user(self.__env)
        }))
        self.__doped = True

    def nope(self) -> None:
        if self.__doped or self.__noped:
            return
        self.__web_socket_client.send(WebSocketMessage(label='thumbsDown', payload={
            'roomId': self.__env.get_jqbx_room_id(),
            'user': get_bot_user(self.__env)
        }))
        self.__noped = True

    @property
    def welcome_message(self) -> Optional[str]:
        return self.__welcome_message

    @property
    def doped(self) -> bool:
        return self.__doped

    @property
    def noped(self) -> bool:
        return self.__noped

    def set_welcome_message(self, welcome_message: Optional[str]) -> None:
        self.__welcome_message = welcome_message

    def reset_vote(self) -> None:
        self.__doped = False
        self.__noped = False
