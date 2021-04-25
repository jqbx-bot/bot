from typing import Optional, List, Dict

from src.data_service import AbstractDataService


class FakeDataService(AbstractDataService):

    def __init__(self):
        self.__welcome_message: Optional[str] = None

    def get_welcome_message(self) -> Optional[str]:
        return self.__welcome_message

    def set_welcome_message(self, welcome_message: str) -> None:
        self.__welcome_message = welcome_message

    def clear_welcome_message(self) -> None:
        self.__welcome_message = None

    def relink(self, track_id: str, markets: List[str]) -> Optional[Dict[str, str]]:
        return None
