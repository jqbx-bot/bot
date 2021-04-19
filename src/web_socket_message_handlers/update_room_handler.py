from typing import List

from src.bot_controller import AbstractBotController, BotController
from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler


class UpdateRoomHandler(AbstractWebSocketMessageHandler):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
                 room_state: AbstractRoomState = RoomState.get_instance()):
        self.__bot_controller = bot_controller
        self.__room_state = room_state

    @property
    def message_label(self) -> str:
        return 'update-room'

    def handle(self, message: WebSocketMessage) -> None:
        payload = message.payload
        self.__update_mod_ids(payload)
        self.__welcome_and_update_users(message.payload)
        self.__update_track(payload)
        self.__update_room_title(payload)

    def __update_mod_ids(self, payload: dict) -> None:
        admins = payload.get('admin', [])
        mods = payload.get('mods', [])
        if admins + mods:
            self.__room_state.set_mod_ids([x.split(':')[-1] for x in list(set(admins + mods))])

    def __welcome_and_update_users(self, payload: dict) -> None:
        users: List[dict] = payload.get('users', [])
        if self.__room_state.user_ids and self.__bot_controller.welcome_message:
            for new_user in [x for x in users if x['id'] not in self.__room_state.user_ids]:
                self.__bot_controller.whisper(
                    self.__bot_controller.welcome_message,
                    {'uri': 'spotify:user:%s' % new_user['id'], 'username': new_user['username']}
                )
        self.__room_state.set_user_ids(list(set([x['id'] for x in users])))

    def __update_track(self, payload: dict) -> None:
        tracks = payload.get('tracks', [])
        if tracks:
            self.__room_state.set_current_track(tracks[0])

    def __update_room_title(self, payload: dict) -> None:
        room_title = payload.get('title')
        if room_title:
            self.__room_state.set_room_title(room_title)
