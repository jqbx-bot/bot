from typing import Optional

from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor


class SureJanCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance()):
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'sj'

    @property
    def help(self) -> str:
        return 'Sure, Jan.'

    def process(self, user_id: str, payload: Optional[str]) -> None:
        self.__bot_controller.chat('https://media.giphy.com/media/1AIeYgwnqeBUxh6juu/giphy.gif')
