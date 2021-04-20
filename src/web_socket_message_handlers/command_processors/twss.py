import random
from typing import Optional, List

from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor


class ThatsWhatSheSaidCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance()):
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'twss'

    @property
    def help(self) -> str:
        return 'That\'s what she said.'

    def process(self, user_id: str, payload: Optional[str]) -> None:
        gifs: List[str] = [
            'https://media.giphy.com/media/IjJ8FVe4HVk66yvlV2/giphy.gif',
            'https://media.giphy.com/media/esR1eKgmOnxWKR627f/giphy.gif',
            'https://media.giphy.com/media/Zgo2A2oOpbGhQdf09T/giphy.gif',
            'https://media.giphy.com/media/IJLVLpZQuS4z6/giphy.gif',
            'https://media.giphy.com/media/4YPXOIVxBOlHPJTbCY/giphy.gif',
            'https://media.giphy.com/media/aSNptUx8RNJiJV2ztv/giphy.gif',
            'https://media.giphy.com/media/4ZfeknJaIiITfHn3ag/giphy.gif,'
            'https://media.giphy.com/media/elPiadNl05XWg/giphy.gif'
        ]
        random.shuffle(gifs)
        self.__bot_controller.chat(random.choice(gifs))
