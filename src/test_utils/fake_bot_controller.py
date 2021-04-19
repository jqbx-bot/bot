from typing import Optional, List

from src.bot_controller import AbstractBotController


class FakeBotController(AbstractBotController):

    def __init__(self):
        self.__welcome_message: Optional[str] = None
        self.__chats: List[str] = []
        self.__doped: bool = False
        self.__noped: bool = False

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

    def chat(self, message: str, recipients: Optional[List[dict]] = None) -> None:
        self.__chats.append(message)

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
