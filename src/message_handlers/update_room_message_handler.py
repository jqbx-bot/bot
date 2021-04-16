from typing import List

from src.abstract_bot import AbstractBot
from src.bot_state import BotState
from src.message import Message
from src.message_handlers.abstract_message_handler import AbstractMessageHandler


class UpdateRoomMessageHandler(AbstractMessageHandler):
    def handle(self, bot: AbstractBot, state: BotState, message: Message) -> None:
        payload = message.payload
        self.__update_mod_ids(state, payload)
        self.__welcome_new_users(bot, state, payload)
        self.__update_user_ids(state, payload)

    @staticmethod
    def __update_mod_ids(state: BotState, payload: dict) -> None:
        admins: List[str] = payload['admin']
        mods: List[str] = payload['mods']
        mod_ids = [x.split(':')[-1] for x in list(set(admins + mods))]
        state.set_mod_ids(mod_ids)

    @staticmethod
    def __update_user_ids(state: BotState, payload: dict) -> None:
        state.set_user_ids(list(set([x['id'] for x in payload['users']])))

    @staticmethod
    def __welcome_new_users(bot: AbstractBot, state: BotState, payload: dict) -> None:
        if not state.welcome_message:
            return
        new_users = [x for x in payload['users'] if x['id'] not in state.user_ids]
        for new_user in new_users:
            bot.chat('/whisper @%s %s' % (new_user['username'], state.welcome_message))
