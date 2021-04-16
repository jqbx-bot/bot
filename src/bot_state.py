from typing import List, Optional


class BotState:
    def __init__(self):
        self.__mod_ids: List[str] = []
        self.__user_ids: List[str] = []
        self.__welcome_message: Optional[str] = None

    @property
    def mod_ids(self) -> List[str]:
        return self.__mod_ids

    def set_mod_ids(self, mod_ids: List[str]) -> None:
        self.__mod_ids = mod_ids

    @property
    def user_ids(self) -> List[str]:
        return self.__user_ids

    def set_user_ids(self, user_ids: List[str]) -> None:
        self.__user_ids = user_ids

    @property
    def welcome_message(self) -> Optional[str]:
        return self.__welcome_message

    def set_welcome_message(self, welcome_message: Optional[str]) -> None:
        self.__welcome_message = welcome_message.strip() if welcome_message else None
