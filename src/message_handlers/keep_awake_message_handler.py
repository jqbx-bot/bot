from src.abstract_bot import AbstractBot
from src.bot_state import BotState
from src.message import Message
from src.message_handlers.abstract_message_handler import AbstractMessageHandler


class KeepAwakeMessageHandler(AbstractMessageHandler):
    def handle(self, bot: AbstractBot, state: BotState, message: Message) -> None:
        bot.send(Message(message.code, 'stayAwake', {'date': message.payload['date']}))
