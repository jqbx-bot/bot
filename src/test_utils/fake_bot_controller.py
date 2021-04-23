from typing import Optional, List, Union

from src.bot_controller import AbstractBotController


class FakeBotController(AbstractBotController):

    def __init__(self):
        self.__chats: List[str] = []
        self.__whispers: List[str] = []
        self.__doped: bool = False
        self.__noped: bool = False

    @property
    def doped(self) -> bool:
        return self.__doped

    @property
    def noped(self) -> bool:
        return self.__noped

    def chat(self, message: Union[str, List[str]]) -> None:
        messages: List[str] = message if isinstance(message, list) else [message]
        self.__chats.append('<br/>'.join(messages))

    def whisper(self, message: str, recipient: dict) -> None:
        self.__whispers.append('@%s %s' % (recipient['username'], message))

    def dope(self) -> None:
        self.__doped = True

    def nope(self) -> None:
        self.__noped = True

    def reset_vote(self) -> None:
        self.__doped = False
        self.__noped = False

    def dequeue_chats(self) -> List[str]:
        chats = list(self.__chats)
        self.__chats = []
        return chats

    def dequeue_whispers(self) -> List[str]:
        whispers = list(self.__whispers)
        self.__whispers = []
        return whispers
