from typing import List, Dict


from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.web_socket_message_handlers.command_processors.command_processors import command_processors
from src.web_socket_message_handlers.command_processors.help import HelpCommandProcessor
from src.env import AbstractEnvironment, Environment
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler


class PushMessageHandler(AbstractWebSocketMessageHandler):
    def __init__(self, env: AbstractEnvironment = Environment(),
                 _command_processors: List[AbstractCommandProcessor] = None):
        self.__env = env
        self.__command_processors: Dict[str, AbstractCommandProcessor] = {
            x.keyword: x for x in _command_processors or (command_processors + [HelpCommandProcessor()])
        }

    @property
    def message_label(self) -> str:
        return 'push-message'

    def handle(self, message: WebSocketMessage) -> None:
        payload = message.payload
        user_id = payload.get('user', {}).get('id', None)
        if user_id is None or user_id == self.__env.get_spotify_user_id():
            return
        stripped = payload['message'].strip()
        if not (stripped.startswith('/') and len(stripped) > 1):
            return

        parts = stripped.split(' ', 1)
        keyword = parts[0].lower().split('/', 1)[-1]
        payload = None if len(parts) == 1 else parts[1]

        command_processor = self.__command_processors.get(keyword)
        if command_processor:
            command_processor.process(user_id, payload)
