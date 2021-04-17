from typing import Optional, List, Callable

from src.abstract_bot import AbstractBot


class VoteProcessor:
    def __init__(self, ack_word: str, success_message: str):
        self.__current_track: Optional[dict] = None
        self.__voter_ids: List[str] = []
        self.__ack_word = ack_word
        self.__success_message = success_message

    def process(self, bot: AbstractBot, user_id: str, success_action: Callable[[], None]) -> None:
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
            self.__voter_ids = []
        if user_id in self.__voter_ids:
            bot.chat('You\'ve already voted')
            return
        self.__voter_ids.append(user_id)
        voter_count = len(self.__voter_ids)
        if voter_count <= 2:
            bot.chat(', '.join(self.__ack_word for _ in range(voter_count)))
        elif voter_count == 3:
            bot.chat(self.__success_message)
            success_action()
