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

    def process(self, bot: AbstractBot, user_id: str, payload: Optional[str] = None) -> None:
        is_mod = user_id in bot.mod_ids
        if not payload:
            if bot.welcome_message:
                bot.chat('The current welcome message is: "%s"' % bot.welcome_message)
            else:
                message = 'The welcome message is not currently set.'
                if is_mod:
                    message += ' To set one, type `/welcome [message]`.'
                bot.chat(message)
            return
        if not is_mod:
            bot.chat('Only mods can update the welcome message!')
            return
        bot.set_welcome_message(payload)
        bot.chat('The welcome message has been set to: "%s"' % payload)
