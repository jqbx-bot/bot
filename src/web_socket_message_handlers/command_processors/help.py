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
        for key in sorted(self.__commands.keys()):
            command = self.__commands[key]
            self.__bot_controller.chat('/%s: %s' % (command.keyword, command.help))
