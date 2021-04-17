from typing import Optional

from src.abstract_bot import AbstractBot
from src.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.command_processors.vote_processor import VoteProcessor


class NockOutCommandProcessor(AbstractCommandProcessor):
    def __init__(self):
        self.__vote_processor = VoteProcessor('no', 'no, no, no :-1: no way José!')

    @property
    def keyword(self) -> str:
        return 'no'

    @property
    def help(self) -> str:
        return '''
            Votes for the bot to downvote (nope) a song. Requires 3 people.
        '''

    def process(self, bot: AbstractBot, user_id: str, payload: Optional[str] = None) -> None:
        self.__vote_processor.process(bot, user_id, bot.nope)
