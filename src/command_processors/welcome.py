from typing import Optional

from src.abstract_bot import AbstractBot
from src.bot_state import BotState
from src.command_processors.abstract_command_processor import AbstractCommandProcessor


class WelcomeCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'welcome'

    def process(self, bot: AbstractBot, state: BotState, user_id: str, payload: Optional[str]) -> None:
        if user_id not in state.mod_ids:
            bot.chat('Only mods can do that!')
            return
        if not payload:
            if state.welcome_message:
                bot.chat('The current welcome message is: "%s"' % state.welcome_message)
            else:
                bot.chat('The welcome message is not currently set. To set one, use the command `/welcome [message]`')
            return
        state.set_welcome_message(payload)
        bot.chat('Welcome message set to: "%s"' % payload)
