import json
from typing import Dict

from websocket import WebSocketApp

from src.abstract_bot import AbstractBot
from src.bot_state import BotState
from src.env import AbstractEnvironment
from src.message import Message
from src.message_handlers.abstract_message_handler import AbstractMessageHandler
from src.message_handlers.keep_awake_message_handler import KeepAwakeMessageHandler
from src.message_handlers.push_message_handler import PushMessageHandler
from src.message_handlers.update_room_message_handler import UpdateRoomMessageHandler


class Bot(AbstractBot):
    def __init__(self, env: AbstractEnvironment, state: BotState):
        self.__env = env
        self.__state = state
        self.__ws = WebSocketApp(
            'wss://jqbx.fm/socket.io/?EIO=3&transport=websocket',
            on_open=lambda _: self.__on_open(),
            on_message=lambda _, raw_message: self.__on_message(raw_message)
        )

    def run(self):
        self.__ws.run_forever()

    def send(self, message: Message) -> None:
        serialized = '%s["%s"' % (message.code, message.label)
        if message.payload is not None:
            serialized += ',%s' % json.dumps(message.payload)
        serialized += ']'
        self.__ws.send(serialized)

    def chat(self, message: str) -> None:
        print('%s: %s' % (self.__env.get_jqbx_bot_display_name(), message))
        self.send(Message(42, 'chat', {
            'roomId': self.__env.get_jqbx_room_id(),
            'user': {
                'username': self.__env.get_jqbx_bot_display_name(),
                'id': self.__env.get_spotify_user_id(),
                'uri': 'spotify:user:%s' % self.__env.get_spotify_user_id(),
                'image': self.__env.get_jqbx_bot_image_url(),
                'device': 'bot',
                'status': 'active',
                'country': 'US'
            },
            'message': {
                'message': message,
                'user': {
                    'display_name': self.__env.get_jqbx_bot_display_name(),
                    'id': self.__env.get_spotify_user_id(),
                    'uri': 'spotify:user:%s' % self.__env.get_spotify_user_id(),
                    'username': self.__env.get_jqbx_bot_display_name(),
                    'active': True
                },
                'selectingEmoji': False
            }
        }))

    def __on_open(self) -> None:
        self.send(Message(42, 'join', {
            'roomId': self.__env.get_jqbx_room_id(),
            'user': {
                'username': self.__env.get_jqbx_bot_display_name(),
                'id': self.__env.get_spotify_user_id(),
                'uri': 'spotify:user:%s' % self.__env.get_spotify_user_id(),
                'device': 'bot',
                'status': 'active',
                'country': 'US',
                'image': self.__env.get_jqbx_bot_image_url()
            }
        }))

    def __on_message(self, raw_message: str) -> None:
        message = Message.parse(raw_message)
        handlers: Dict[str, AbstractMessageHandler] = {
            'keepAwake': KeepAwakeMessageHandler(),
            'update-room': UpdateRoomMessageHandler(),
            'push-message': PushMessageHandler(self.__env)
        }
        handler = handlers.get(message.label, None)
        if handler:
            handler.handle(self, self.__state, message)
