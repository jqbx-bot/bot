from typing import Optional, List

from src.bot_controller import AbstractBotController, BotController
from src.room_state import AbstractRoomState, RoomState
from src.spotify_client import AbstractSpotifyClient, SpotifyClient
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor


class RelinkCommandProcessor(AbstractCommandProcessor):
    def __init__(self, spotify_client: AbstractSpotifyClient = SpotifyClient.get_instance(),
                 room_state: AbstractRoomState = RoomState.get_instance(),
                 bot_controller: AbstractBotController = BotController.get_instance()):
        self.__spotify_client = spotify_client
        self.__room_state = room_state
        self.__bot_controller = bot_controller

    @property
    def keyword(self) -> str:
        return 'relink'

    @property
    def help(self) -> str:
        return '''
            If a song is not available to your country, find links to international versions.
        '''

    def process(self, user_id: str, payload: Optional[str] = None) -> None:
        countries: List[str] = list(set([x['country'] for x in self.__room_state.users]))
        international_versions = self.__spotify_client.find_links_to_international_versions(
            self.__room_state.current_track['id'], countries)
        if not international_versions:
            self.__bot_controller.chat('I can\'t find international versions of this track.')
            return
        self.__bot_controller.chat(
            ['These links should be playable:'] +
            ['%s - %s' % (k, v) for k, v in international_versions.items()]
        )
