from typing import Optional

from src.abstract_bot import AbstractBot
from src.command_processors.abstract_command_processor import AbstractCommandProcessor


class FakeCommandProcessor(AbstractCommandProcessor):

    def __init__(self):
        self.__call_user_id: Optional[str] = None
        self.__call_payload: Optional[str] = None
        self.__was_called: bool = False
    @property
    def help(self) -> str:
        return ''

    @property
    def keyword(self) -> str:
        return 'fake'

    @property
    def call_user_id(self) -> Optional[str]:
        return self.__call_user_id

    @property
    def was_called(self) -> bool:
        return self.__was_called

    @property
    def call_payload(self) -> Optional[str]:
        return self.__call_payload

    def process(self, bot: AbstractBot, user_id: str, payload: Optional[str]) -> None:
        self.__call_user_id = user_id
        self.__call_payload = payload
        self.__was_called = True
