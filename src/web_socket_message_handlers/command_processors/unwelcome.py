from typing import Optional

from src.bot_controller import AbstractBotController, BotController
from src.data_service import DataService, AbstractDataService
from src.web_socket_message_handlers.command_processors.abstract_command_processor import AbstractCommandProcessor
from src.room_state import AbstractRoomState, RoomState


class UnwelcomeCommandProcessor(AbstractCommandProcessor):
    def __init__(self, bot_controller: AbstractBotController = BotController.get_instance(),
                 room_state: AbstractRoomState = RoomState.get_instance(),
                 data_service: AbstractDataService = DataService()):
        self.__bot_controller = bot_controller
        self.__room_state = room_state
        self.__data_service = data_service

    @property
    def keyword(self) -> str:
        return 'unwelcome'

    @property
    def help(self) -> str:
        return 'Clear the welcome message'

    def process(self, user_id: str, payload: Optional[str]) -> None:
        if user_id not in self.__room_state.mod_ids:
            self.__bot_controller.chat('Only mods can do that!')
            return
        self.__data_service.clear_welcome_message()
        self.__bot_controller.chat('The welcome message has been cleared.')
