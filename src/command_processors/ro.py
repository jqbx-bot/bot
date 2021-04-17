from typing import Optional, List

from src.abstract_bot import AbstractBot
from src.command_processors.abstract_command_processor import AbstractCommandProcessor


class RockOutCommandProcessor(AbstractCommandProcessor):
    def __init__(self):
        self.__current_track: Optional[dict] = None
        self.__rower_ids: List[str] = []

    @property
    def keyword(self) -> str:
        return 'ro'

    @property
    def help(self) -> str:
        return '''
            Votes for the bot to rock out (dope) a song. Requires 3 people.
        '''

    def process(self, bot: AbstractBot, user_id: str, payload: Optional[str] = None) -> None:
        if not bot.current_track:
            return
        if self.__current_track is None or self.__current_track['id'] != bot.current_track['id']:
            self.__current_track = bot.current_track
            self.__rower_ids = []
        if user_id in self.__rower_ids:
            return
        self.__rower_ids.append(user_id)
        rower_count = len(self.__rower_ids)
        if rower_count <= 2:
            bot.chat(', '.join('row' for _ in range(rower_count)))
        elif rower_count == 3:
            bot.chat('row, row, row your :canoe: gently down the stream')
            bot.dope()
