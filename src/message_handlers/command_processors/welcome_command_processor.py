from typing import Optional

from src.abstract_bot import AbstractBot
from src.bot_state import BotState
from src.message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor


class WelcomeCommandProcessor(AbstractCommandProcessor):
    def process(self, bot: AbstractBot, state: BotState, payload: Optional[str]) -> None:
        if not payload:
            if state.welcome_message:
                bot.chat('The current welcome message is: "Welcome [user(s)]! %s"' % state.welcome_message)
            else:
                bot.chat('The welcome message is not currently set. To set one, use the command `/welcome [message]`')
            return
        state.set_welcome_message(payload)
        bot.chat('Welcome message set to: "Welcome [user(s)]! %s"' % payload)