from typing import List

from src.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.command_processors.dadjoke import DadjokeCommandProcessor
from src.command_processors.ro import RockOutCommandProcessor
from src.command_processors.unwelcome import UnwelcomeCommandProcessor
from src.command_processors.welcome import WelcomeCommandProcessor

command_processors: List[AbstractCommandProcessor] = [
    WelcomeCommandProcessor(),
    UnwelcomeCommandProcessor(),
    DadjokeCommandProcessor(),
    RockOutCommandProcessor()
]
