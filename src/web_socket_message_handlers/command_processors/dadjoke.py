from typing import Optional

from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from dadjokes import dadjokes


class DadjokeCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController()):
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'dadjoke'

    @property
    def help(self) -> str:
        return 'Get a dad joke! Will give a random joke if you do not use a search term.'

    def process(self, user_id: str, payload: Optional[str]) -> None:
        self.__bot_controller.chat(dadjokes.Dadjoke().joke)
