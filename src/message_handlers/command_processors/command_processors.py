from typing import Dict

from src.message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.message_handlers.command_processors.dadjoke_command_processor import DadjokeCommandProcessor
from src.message_handlers.command_processors.help_command_processor import HelpCommandProcessor
from src.message_handlers.command_processors.unwelcome_command_processor import UnwelcomeCommandProcessor
from src.message_handlers.command_processors.welcome_command_processor import WelcomeCommandProcessor

command_processors: Dict[str, AbstractCommandProcessor] = {
    '/welcome': WelcomeCommandProcessor(),
    '/unwelcome': UnwelcomeCommandProcessor(),
    '/dadjoke': DadjokeCommandProcessor(),
    '/help': HelpCommandProcessor()
}
