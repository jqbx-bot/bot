from typing import Dict, Callable, List

from src.abstract_bot import AbstractBot
from src.bot_state import BotState
from src.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.command_processors.help import HelpCommandProcessor
from src.env import AbstractEnvironment
from src.web_socket_client import AbstractWebSocketClient
from src.web_socket_message import WebSocketMessage


class Bot(AbstractBot):
    def __init__(self, env: AbstractEnvironment, state: BotState, web_socket_client: AbstractWebSocketClient,
                 command_processors: List[AbstractCommandProcessor]):
        self.__env = env
        self.__state = state
        self.__command_processors: Dict[str, AbstractCommandProcessor] = {
            x.keyword: x for x in command_processors + [HelpCommandProcessor()]
        }
        self.__web_socket_client = web_socket_client
        web_socket_client.register(self.__on_open, self.__on_message)

    def run(self):
        self.__web_socket_client.run()

    def chat(self, message: str) -> None:
        self.__web_socket_client.send(WebSocketMessage(42, 'chat', {
            'roomId': self.__env.get_jqbx_room_id(),
            'user': self.__get_bot_user(),
            'message': {
                'message': message,
                'user': self.__get_bot_user(),
                'selectingEmoji': False
            }
        }))

    def __on_open(self) -> None:
        self.__web_socket_client.send(WebSocketMessage(42, 'join', {
            'roomId': self.__env.get_jqbx_room_id(),
            'user': self.__get_bot_user()
        }))

    def __on_message(self, message: WebSocketMessage) -> None:
        handlers: Dict[str, Callable[[WebSocketMessage], None]] = {
            'keepAwake': self.__handle_keep_awake_message,
            'update-room': self.__handle_update_room_message,
            'push-message': self.__handle_push_message
        }
        handler = handlers.get(message.label, None)
        if handler:
            handler(message)

    def __handle_keep_awake_message(self, message: WebSocketMessage) -> None:
        self.__web_socket_client.send(WebSocketMessage(message.code, 'stayAwake', {'date': message.payload['date']}))

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
            command_processor.process(self, self.__state, user_id, payload)

    def __handle_update_room_message(self, message: WebSocketMessage) -> None:
        self.__update_mod_ids(message.payload)
        self.__welcome_and_update_users(message.payload)

    def __update_mod_ids(self, payload: dict) -> None:
        self.__state.set_mod_ids([x.split(':')[-1] for x in list(set(payload['admin'] + payload['mods']))])

    def __welcome_and_update_users(self, payload: dict) -> None:
        if self.__state.user_ids and self.__state.welcome_message:
            for new_user in [x for x in payload['users'] if x['id'] not in self.__state.user_ids]:
                self.chat('@%s %s' % (new_user['username'], self.__state.welcome_message))
        self.__state.set_user_ids(list(set([x['id'] for x in payload['users']])))

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
