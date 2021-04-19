from src.room_state import AbstractRoomState, RoomState
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler


class PlayTrackHandler(AbstractWebSocketMessageHandler):
    def __init__(self, room_state: AbstractRoomState = RoomState.get_instance()):
        self.__room_state = room_state

    @property
    def message_label(self) -> str:
        return 'play-track'

    def handle(self, message: WebSocketMessage) -> None:
        self.__room_state.set_current_track(message.payload)
