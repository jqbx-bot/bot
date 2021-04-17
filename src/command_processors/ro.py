from typing import Optional, List

from src.abstract_bot import AbstractBot
from src.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.command_processors.vote_processor import VoteProcessor


class RockOutCommandProcessor(AbstractCommandProcessor):
    def __init__(self):
        self.__vote_processor = VoteProcessor('row', 'row, row, row your :canoe: gently down the stream')

    @property
    def keyword(self) -> str:
        return 'ro'

    @property
    def help(self) -> str:
        return '''
            Votes for the bot to rock out (dope) a song. Requires 3 people.
        '''

    def process(self, bot: AbstractBot, user_id: str, payload: Optional[str] = None) -> None:
        self.__vote_processor.process(bot, user_id, bot.dope)