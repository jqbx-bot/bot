from src.abstract_bot import AbstractBot
from src.bot_state import BotState
from src.env import AbstractEnvironment
from src.message import Message
from src.message_handlers.abstract_message_handler import AbstractMessageHandler
from src.message_handlers.command_processors.command_processors import command_processors


class PushMessageHandler(AbstractMessageHandler):
    def __init__(self, env: AbstractEnvironment):
        self.__env = env

    def handle(self, bot: AbstractBot, state: BotState, message: Message) -> None:
        payload = message.payload
        user_id = payload['user']['id']
        if user_id == self.__env.get_spotify_user_id():
            return
        stripped = payload['message'].strip()
        if not (stripped.startswith('/') and len(stripped) > 1):
            return

        parts = stripped.split(' ', 1)
        command = parts[0]
        payload = None if len(parts) == 1 else parts[1]

        command_processor = command_processors.get(command, None)
        if command_processor:
            command_processor.process(bot, state, user_id, payload)



