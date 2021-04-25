from typing import Optional

from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from dadjokes import dadjokes


class DadjokeCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance()):
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'dadjoke'

    @property
    def help(self) -> str:
        return 'Hi, I\'m Dad.'

    def process(self, user_id: str, payload: Optional[str]) -> None:
        self.__bot_controller.chat(dadjokes.Dadjoke().joke)
