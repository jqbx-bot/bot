from typing import Optional

from src.abstract_bot import AbstractBot
from src.command_processors.abstract_command_processor import AbstractCommandProcessor


class WelcomeCommandProcessor(AbstractCommandProcessor):
    @property
    def keyword(self) -> str:
        return 'welcome'

    @property
    def help(self) -> str:
        return '''
            Set a welcome message (or just display the current message if new message not provided)
        '''

    def process(self, bot: AbstractBot, user_id: str, payload: Optional[str]) -> None:
        if user_id not in bot.mod_ids:
            bot.chat('Only mods can do that!')
            return
        if not payload:
            if bot.welcome_message:
                bot.chat('The current welcome message is: "%s"' % bot.welcome_message)
            else:
                bot.chat('The welcome message is not currently set. To set one, use the command `/welcome [message]`')
            return
        bot.set_welcome_message(payload)
        bot.chat('Welcome message set to: "%s"' % payload)
