from typing import Optional

from src.abstract_bot import AbstractBot
from src.bot_state import BotState
from src.message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor


class UnwelcomeCommandProcessor(AbstractCommandProcessor):
    def process(self, bot: AbstractBot, state: BotState, user_id: str, payload: Optional[str]) -> None:
        if user_id not in state.mod_ids:
            bot.chat('Only mods can do that!')
            return
        state.set_welcome_message(None)
        bot.chat('The welcome message has been cleared.')