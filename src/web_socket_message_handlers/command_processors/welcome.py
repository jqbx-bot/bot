from typing import Optional

from src.bot_controller import AbstractBotController, BotController
from src.data_service import DataService, AbstractDataService
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.room_state import AbstractRoomState, RoomState


class WelcomeCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
                 room_state: AbstractRoomState = RoomState.get_instance(),
                 data_service: AbstractDataService = DataService()):
        self.__bot_controller = bot_controller
        self.__room_state = room_state
        self.__data_service = data_service

    @property
    def keyword(self) -> str:
        return 'welcome'

    @property
    def help(self) -> str:
        return '''
            Set a welcome message (or just display the current message if new message not provided)
        '''

    def process(self, user_id: str, payload: Optional[str] = None) -> None:
        is_mod = user_id in self.__room_state.mod_ids
        if not payload:
            current_welcome_message = self.__data_service.get_welcome_message()
            if current_welcome_message:
                self.__bot_controller.chat('The current welcome message is: "%s"' % current_welcome_message)
            else:
                chat_message = 'The welcome message is not currently set.'
                if is_mod:
                    chat_message += ' To set one, type `/welcome [message]`.'
                self.__bot_controller.chat(chat_message)
            return
        if not is_mod:
            self.__bot_controller.chat('Only mods can update the welcome message!')
            return
        self.__data_service.set_welcome_message(payload)
        self.__bot_controller.chat('The welcome message has been set to: "%s"' % payload)
