from typing import Dict, Callable, List, Optional

from src.abstract_bot import AbstractBot
from src.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.command_processors.help import HelpCommandProcessor
from src.env import AbstractEnvironment
from src.web_socket_client import AbstractWebSocketClient
from src.web_socket_message import WebSocketMessage


class Bot(AbstractBot):
    def __init__(self, env: AbstractEnvironment, web_socket_client: AbstractWebSocketClient,
                 command_processors: List[AbstractCommandProcessor]):
        self.__env = env
        self.__mod_ids: List[str] = []
        self.__user_ids: List[str] = []
        self.__welcome_message: Optional[str] = None
        self.__current_track: Optional[dict] = None
        self.__doped: bool = False
        self.__noped: bool = False
        self.__command_processors: Dict[str, AbstractCommandProcessor] = {
            x.keyword: x for x in command_processors + [HelpCommandProcessor()]
        }
        self.__web_socket_client = web_socket_client
        web_socket_client.register(self.__on_open, self.__on_message)

    @property
    def mod_ids(self) -> List[str]:
        return self.__mod_ids

    @property
    def welcome_message(self) -> Optional[str]:
        return self.__welcome_message

    @property
    def current_track(self) -> Optional[dict]:
        return self.__current_track

    @property
    def doped(self) -> bool:
        return self.__doped

    @property
    def noped(self) -> bool:
        return self.__noped

    def set_welcome_message(self, welcome_message: Optional[str]) -> None:
        self.__welcome_message = welcome_message

    def run(self):
        self.__web_socket_client.run()

    def chat(self, message: str, recipients: Optional[List[dict]] = None) -> None:
        payload = {
            'roomId': self.__env.get_jqbx_room_id(),
            'user': self.__get_bot_user(),
            'message': {
                'message': message,
                'user': self.__get_bot_user(),
                'selectingEmoji': False
            }
        }
        if recipients:
            payload['message']['recipients'] = recipients
        self.__web_socket_client.send(WebSocketMessage(label='chat', payload=payload))

    def dope(self) -> None:
        if self.__doped or self.__noped:
            return
        self.__web_socket_client.send(WebSocketMessage(label='thumbsUp', payload={
            'roomId': self.__env.get_jqbx_room_id(),
            'user': self.__get_bot_user()
        }))
        self.__doped = True

    def nope(self) -> None:
        if self.__doped or self.__noped:
            return
        self.__web_socket_client.send(WebSocketMessage(label='thumbsDown', payload={
            'roomId': self.__env.get_jqbx_room_id(),
            'user': self.__get_bot_user()
        }))
        self.__noped = True

    def __on_open(self) -> None:
        self.__web_socket_client.send(WebSocketMessage(label='join', payload={
            'roomId': self.__env.get_jqbx_room_id(),
            'user': self.__get_bot_user()
        }))

    def __on_message(self, message: WebSocketMessage) -> None:
        handlers: Dict[str, Callable[[WebSocketMessage], None]] = {
            'keepAwake': self.__handle_keep_awake_message,
            'update-room': self.__handle_update_room_message,
            'push-message': self.__handle_push_message,
            'play-track': self.__handle_play_track
        }
        handler = handlers.get(message.label, None)
        if handler:
            handler(message)

    def __handle_keep_awake_message(self, message: WebSocketMessage) -> None:
        self.__web_socket_client.send(WebSocketMessage(label='stayAwake', payload={'date': message.payload['date']}))
        self.__web_socket_client.send(WebSocketMessage(2))

    def __handle_push_message(self, message: WebSocketMessage) -> None:
        payload = message.payload
        user_id = payload['user']['id']
        if user_id == self.__env.get_spotify_user_id():
            return
        stripped = payload['message'].strip()
        if not (stripped.startswith('/') and len(stripped) > 1):
            return

        parts = stripped.split(' ', 1)
        keyword = parts[0].lower().split('/', 1)[-1]
        payload = None if len(parts) == 1 else parts[1]

        command_processor = self.__command_processors.get(keyword)
        if command_processor:
            command_processor.process(self, user_id, payload)

    def __handle_update_room_message(self, message: WebSocketMessage) -> None:
        payload = message.payload
        self.__mod_ids = [x.split(':')[-1] for x in list(set(payload.get('admin', []) + payload.get('mods', [])))]
        self.__welcome_and_update_users(message.payload)
        tracks = payload.get('tracks', [])
        if tracks:
            self.__handle_track_change(tracks[0])

    def __welcome_and_update_users(self, payload: dict) -> None:
        users: List[dict] = payload.get('users', [])
        if self.__user_ids and self.__welcome_message:
            for new_user in [x for x in users if x['id'] not in self.__user_ids]:
                self.chat(
                    '@%s %s' % (new_user['username'], self.__welcome_message),
                    [{'uri': 'spotify:user:%s' % new_user['id']}]
                )
        self.__user_ids = list(set([x['id'] for x in users]))

    def __handle_play_track(self, message: WebSocketMessage) -> None:
        self.__handle_track_change(message.payload)

    def __handle_track_change(self, new_track: dict) -> None:
        self.__current_track = new_track
        self.__doped = False
        self.__noped = False

    def __get_bot_user(self) -> dict:
        return {
            'username': self.__env.get_jqbx_bot_display_name(),
            'id': self.__env.get_spotify_user_id(),
            'uri': 'spotify:user:%s' % self.__env.get_spotify_user_id(),
            'device': 'bot',
            'status': 'active',
            'country': 'US',
            'image': self.__env.get_jqbx_bot_image_url()
        }
