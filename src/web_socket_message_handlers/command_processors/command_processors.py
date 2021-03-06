from typing import List

from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.choose import ChooseCommandProcessor
from src.web_socket_message_handlers.command_processors.dadjoke import DadjokeCommandProcessor
from src.web_socket_message_handlers.command_processors.mbn import MustBeNiceCommandProcessor
from src.web_socket_message_handlers.command_processors.no import NockOutCommandProcessor
from src.web_socket_message_handlers.command_processors.relink import RelinkCommandProcessor
from src.web_socket_message_handlers.command_processors.ro import RockOutCommandProcessor
from src.web_socket_message_handlers.command_processors.sj import SureJanCommandProcessor
from src.web_socket_message_handlers.command_processors.theme import ThemeCommandProcessor
from src.web_socket_message_handlers.command_processors.twss import ThatsWhatSheSaidCommandProcessor
from src.web_socket_message_handlers.command_processors.unwelcome import UnwelcomeCommandProcessor
from src.web_socket_message_handlers.command_processors.urban import UrbanCommandProcessor
from src.web_socket_message_handlers.command_processors.welcome import WelcomeCommandProcessor

command_processors: List[AbstractCommandProcessor] = [
    WelcomeCommandProcessor(),
    UnwelcomeCommandProcessor(),
    DadjokeCommandProcessor(),
    RockOutCommandProcessor(),
    NockOutCommandProcessor(),
    UrbanCommandProcessor(),
    SureJanCommandProcessor(),
    MustBeNiceCommandProcessor(),
    ThatsWhatSheSaidCommandProcessor(),
    ChooseCommandProcessor(),
    ThemeCommandProcessor(),
    RelinkCommandProcessor()
]
