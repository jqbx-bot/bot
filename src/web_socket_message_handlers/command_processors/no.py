from typing import Optional

from src.bot_controller import AbstractBotController
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.voting_machine import VotingMachine


class NockOutCommandProcessor(AbstractCommandProcessor):
    def __init__(self):
        self.__voting_machine = VotingMachine('no')

    @property
    def keyword(self) -> str:
        return 'no'

    @property
    def help(self) -> str:
        return '''
            Votes for the bot to downvote (nope) a song. Requires 3 people.
        '''

    def process(self, user_id: str, payload: Optional[str] = None) -> None:
        self.__voting_machine.vote(user_id, self.__nope)

    def __nope(self, bot_controller: AbstractBotController) -> None:
        bot_controller.nope()
        bot_controller.chat('no, no, no :-1: no way José!')
