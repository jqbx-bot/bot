from typing import Optional

from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.voting_machine import VotingMachine


class RockOutCommandProcessor(AbstractCommandProcessor):
    def __init__(self):
        self.__vote_processor = VotingMachine('row', 'row, row, row your :canoe: gently down the stream')

    @property
    def keyword(self) -> str:
        return 'ro'

    @property
    def help(self) -> str:
        return '''
            Votes for the bot to rock out (dope) a song. Requires 3 people.
        '''

    def process(self, user_id: str, payload: Optional[str] = None) -> None:
        self.__vote_processor.vote(user_id, lambda x: x.dope())
