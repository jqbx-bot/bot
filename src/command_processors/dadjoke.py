from typing import Optional

from src.abstract_bot import AbstractBot
from src.command_processors.abstract_command_processor import AbstractCommandProcessor
from dadjokes import dadjokes


class DadjokeCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'dadjoke'

    @property
    def help(self) -> str:
        return 'Get a dad joke! Will give a random joke if you do not use a search term.'

    def process(self, bot: AbstractBot, user_id: str, payload: Optional[str]) -> None:
        bot.chat(dadjokes.Dadjoke().joke)
