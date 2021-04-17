from typing import Optional

from src.abstract_bot import AbstractBot
from src.bot_state import BotState
from src.command_processors.abstract_command_processor import AbstractCommandProcessor


class HelpCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'help'

    def process(self, bot: AbstractBot, state: BotState, user_id: str, payload: Optional[str]) -> None:
        bot.chat('For a list of bot commmands, see https://github.com/amamparo/jqbx-bot/blob/master/README.md')
