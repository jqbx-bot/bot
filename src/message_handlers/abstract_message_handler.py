from abc import abstractmethod, ABC

from src.abstract_bot import AbstractBot
from src.bot_state import BotState
from src.message import Message


class AbstractMessageHandler(ABC):
    @abstractmethod
    def handle(self, bot: AbstractBot, state: BotState, message: Message) -> None:
        pass
