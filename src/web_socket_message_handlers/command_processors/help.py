from typing import Optional, Dict

from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.command_processors import command_processors


class HelpCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance()):
        self.__commands: Dict[str, AbstractCommandProcessor] = {
            x.keyword: x for x in command_processors
        }
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'help'

    @property
    def help(self) -> str:
        return 'This'

    def process(self, user_id: str, payload: Optional[str]) -> None:
        if not payload:
            self.__empty_help()
        else:
            stripped = payload.strip()
            command = self.__commands.get(stripped, None)
            if command:
                self.__command_help(command)
            else:
                self.__bot_controller.chat('Could not find help details for command `%s`' % stripped)

    def __empty_help(self) -> None:
        sorted_commands = sorted(self.__commands.keys())
        self.__bot_controller.chat(
            'To get help for a specific command, type `/help [command]`.  Available commands: %s' % (
                ', '.join(sorted_commands)
            )
        )

    def __command_help(self, command: AbstractCommandProcessor) -> None:
        self.__bot_controller.chat('/%s: %s' % (command.keyword, command.help))
