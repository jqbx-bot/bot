import random
from typing import Optional

from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor


class ChooseCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance()):
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'choose'

    @property
    def help(self) -> str:
        return 'Pick something randomly from a comma-separated list of choices'

    def process(self, user_id: str, payload: Optional[str]) -> None:
        if not payload:
            self.__bot_controller.chat('Please give me a comma-separate list of choices')
            return
        self.__bot_controller.chat(random.choice(payload.split(',')).strip())
