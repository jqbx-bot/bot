from abc import ABC, abstractmethod
from typing import List, Optional

from src.bot_controller import BotController, AbstractBotController


class AbstractRoomState(ABC):
    @property
    @abstractmethod
    def room_title(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def mod_ids(self) -> List[str]:
        pass

    @property
    @abstractmethod
    def users(self) -> List[dict]:
        pass

    @property
    @abstractmethod
    def current_track(self) -> Optional[dict]:
        pass

    @abstractmethod
    def set_room_title(self, room_title: str) -> None:
        pass

    @abstractmethod
    def set_mod_ids(self, mod_ids: List[str]) -> None:
        pass

    @abstractmethod
    def set_users(self, users: List[dict]) -> None:
        pass

    @abstractmethod
    def set_current_track(self, current_track: dict) -> None:
        pass


class RoomState(AbstractRoomState):
    __instance: Optional['RoomState'] = None

    def __init__(self, bot_controller: AbstractBotController):
        if RoomState.__instance:
            raise Exception('Use get_instance() instead!')
        self.__mod_ids: List[str] = []
        self.__users: List[dict] = []
        self.__current_track: Optional[dict] = None
        self.__bot_controller = bot_controller
        self.__room_title: Optional[str] = None
        RoomState.__instance = self

    @staticmethod
    def get_instance(bot_controller: AbstractBotController = BotController.get_instance()) -> 'RoomState':
        if RoomState.__instance is None:
            RoomState(bot_controller)
        return RoomState.__instance

    @property
    def room_title(self) -> Optional[str]:
        return self.__room_title

    @property
    def mod_ids(self) -> List[str]:
        return self.__mod_ids

    @property
    def users(self) -> List[dict]:
        return self.__users

    @property
    def current_track(self) -> Optional[dict]:
        return self.__current_track

    def set_mod_ids(self, mod_ids: List[str]) -> None:
        self.__mod_ids = mod_ids

    def set_users(self, users: List[dict]) -> None:
        self.__users = users

    def set_current_track(self, current_track: dict) -> None:
        self.__current_track = current_track
        self.__bot_controller.reset_vote()

    def set_room_title(self, room_title: str) -> None:
        self.__room_title = room_title
