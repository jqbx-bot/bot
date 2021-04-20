import random
from typing import Optional, List

from src.bot_controller import AbstractBotController, BotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor


class MustBeNiceCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance()):
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'mbn'

    @property
    def help(self) -> str:
        return 'Must be nice.'

    def process(self, user_id: str, payload: Optional[str]) -> None:
        gifs: List[str] = [
            'https://media.giphy.com/media/l378fAEzVybK1OPYI/giphy.gif',
            'https://media.giphy.com/media/1k3TQPE9gAMpe5wNSV/giphy.gif',
            'https://media.giphy.com/media/fVyY03MV1jruXqSl0q/giphy.gif',
            'https://media.giphy.com/media/l1AvAntv3VFGdd3W0/giphy.gif',
            'https://media.giphy.com/media/77AUQKI6zgRXXg2DBA/giphy.gif',
            'https://media.giphy.com/media/MAvWndHExaLdvghOLT/giphy.gif',
            'https://media1.tenor.com/images/8baae17de0f116f0f632c6faea444e6c/tenor.gif',
            'https://media1.tenor.com/images/25a3f9c90e1984e99f3c58eafe405c62/tenor.gif',
            'https://media1.tenor.com/images/7bf0b70bff3c1670b348146d013c1ef5/tenor.gif'
        ]
        random.shuffle(gifs)
        self.__bot_controller.chat(random.choice(gifs))
