from typing import Optional

from src.bot_controller import AbstractBotController
from src.data_service import DataService, AbstractDataService
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.voting_machine import VotingMachine


class RockOutCommandProcessor(AbstractCommandProcessor):
    def __init__(self, room_state: AbstractRoomState = RoomState.get_instance(),
                 data_service: AbstractDataService = DataService()):
        self.__voting_machine = VotingMachine('row')
        self.__room_state = room_state
        self.__data_service = data_service

    @property
    def keyword(self) -> str:
        return 'ro'

    @property
    def help(self) -> str:
        return '''
            Votes for the bot to rock out (dope) a song. Requires 3 people.
        '''

    def process(self, user_id: str, payload: Optional[str] = None) -> None:
        self.__voting_machine.vote(user_id, self.__dope_and_add_to_playlist)

    def __dope_and_add_to_playlist(self, bot_controller: AbstractBotController) -> None:
        bot_controller.dope()
        bot_controller.chat('row, row, row your :canoe: gently down the stream!')
        playlist_id = self.__data_service.add_to_favorites_playlist(self.__room_state.current_track['id'])
        bot_controller.chat('This track has been added to https://open.spotify.com/playlist/%s' % playlist_id)
