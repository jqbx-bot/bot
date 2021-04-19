from typing import List, Dict

from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler
from src.web_socket_message_handlers.keep_awake_handler import KeepAwakeHandler
from src.web_socket_message_handlers.play_track_handler import PlayTrackHandler
from src.web_socket_message_handlers.push_message_handler import PushMessageHandler
from src.web_socket_message_handlers.update_room_handler import UpdateRoomHandler

web_socket_message_handlers: List[AbstractWebSocketMessageHandler] = [
    KeepAwakeHandler(),
    PlayTrackHandler(),
    PushMessageHandler(),
    UpdateRoomHandler()
]

web_socket_message_handler_map: Dict[str, AbstractWebSocketMessageHandler] = {
    x.message_label: x for x in web_socket_message_handlers
}
