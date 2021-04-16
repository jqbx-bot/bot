from typing import Optional

from src.abstract_bot import AbstractBot
from src.bot_state import BotState
from src.message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from dadjokes import dadjokes

class DadjokeCommandProcessor(AbstractCommandProcessor):
    def process(self, bot: AbstractBot, state: BotState, user_id: str, payload: Optional[str]) -> None:
        bot.chat(dadjokes.Dadjoke().joke)