from typing import Optional

from src.abstract_bot import AbstractBot
from src.command_processors.abstract_command_processor import AbstractCommandProcessor
from dadjokes import dadjokes


class DadjokeCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'dadjoke'

    def process(self, bot: AbstractBot, user_id: str, payload: Optional[str]) -> None:
        bot.chat(dadjokes.Dadjoke().joke)
