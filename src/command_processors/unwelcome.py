from typing import Optional

from src.abstract_bot import AbstractBot
from src.command_processors.abstract_command_processor import AbstractCommandProcessor


class UnwelcomeCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'unwelcome'

    def process(self, bot: AbstractBot, user_id: str, payload: Optional[str]) -> None:
        if user_id not in bot.mod_ids:
            bot.chat('Only mods can do that!')
            return
        bot.set_welcome_message(None)
        bot.chat('The welcome message has been cleared.')
