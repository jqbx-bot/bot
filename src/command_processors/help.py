from typing import Optional, Dict

from src.abstract_bot import AbstractBot
from src.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.command_processors.command_processors import command_processors


class HelpCommandProcessor(AbstractCommandProcessor):
    def __init__(self):
        self.__commands: Dict[str, AbstractCommandProcessor] = {
            x.keyword: x for x in command_processors
        }

    @property
    def keyword(self) -> str:
        return 'help'

    @property
    def help(self) -> str:
        return 'This'

    def process(self, bot: AbstractBot, user_id: str, payload: Optional[str]) -> None:
        if not payload:
            self.__empty_help(bot)
        else:
            stripped = payload.strip()
            command = self.__commands.get(stripped, None)
            if command:
                self.__command_help(bot, command)
            else:
                bot.chat('Could not find help details for command `%s`' % stripped)

    def __empty_help(self, bot: AbstractBot) -> None:
        sorted_commands = sorted(self.__commands.keys())
        bot.chat(
            'To get help for a specific command, type `/help [command]`.  Available commands: %s' % (
                ', '.join(sorted_commands)
            )
        )

    @staticmethod
    def __command_help(bot: AbstractBot, command: AbstractCommandProcessor) -> None:
        bot.chat('/%s - %s' % (command.keyword, command.help))
