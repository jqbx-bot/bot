from typing import Optional, List

from src.abstract_bot import AbstractBot


class FakeBot(AbstractBot):
    def __init__(self):
        self.__mod_ids: List[str] = []
        self.__welcome_message: Optional[str] = None
        self.__chats: List[str] = []
        self.__doped: bool = False
        self.__current_track: Optional[dict] = None

    @property
    def mod_ids(self) -> List[str]:
        return self.__mod_ids

    @property
    def welcome_message(self) -> Optional[str]:
        return self.__welcome_message

    @property
    def current_track(self) -> Optional[dict]:
        return self.__current_track

    @property
    def doped(self) -> bool:
        return self.__doped

    def set_welcome_message(self, welcome_message: Optional[str]) -> None:
        self.__welcome_message = welcome_message

    def run(self) -> None:
        pass

    def chat(self, message: str, recipients: Optional[List[dict]] = None) -> None:
        self.__chats.append(message)

    def dope(self) -> None:
        self.__doped = True

    def set_current_track(self, current_track: dict) -> None:
        self.__current_track = current_track

    def dequeue_chats(self) -> List[str]:
        chats = list(self.__chats)
        self.__chats = []
        return chats
