from typing import Optional, List

from src.abstract_bot import AbstractBot
from src.command_processors.abstract_command_processor import AbstractCommandProcessor


class NockOutCommandProcessor(AbstractCommandProcessor):
    def __init__(self):
        self.__current_track: Optional[dict] = None
        self.__noper_ids: List[str] = []

    @property
    def keyword(self) -> str:
        return 'no'

    @property
    def help(self) -> str:
        return '''
            Votes for the bot to downvote (nope) a song. Requires 3 people.
        '''

    def process(self, bot: AbstractBot, user_id: str, payload: Optional[str] = None) -> None:
        if not bot.current_track:
            return
        if bot.doped:
            bot.chat('I\'m already bopping to this')
            return
        if bot.noped:
            bot.chat('I\'m already hating this')
            return
        if self.__current_track is None or self.__current_track['id'] != bot.current_track['id']:
            self.__current_track = bot.current_track
            self.__noper_ids = []
        if user_id in self.__noper_ids:
            bot.chat('You\'ve already voted')
            return
        self.__noper_ids.append(user_id)
        noper_count = len(self.__noper_ids)
        if noper_count <= 2:
            bot.chat(', '.join('no' for _ in range(noper_count)))
        elif noper_count == 3:
            bot.chat('no, no, no :-1: no way José!')
            bot.nope()
