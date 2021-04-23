from typing import List
from unittest import TestCase

from src.room_state import RoomState
from src.test_utils.fake_bot_controller import FakeBotController
from src.test_utils.fake_data_service import FakeDataService
from src.test_utils.test_helpers import create_random_string
from src.web_socket_message_handlers.command_processors.welcome import WelcomeCommandProcessor


class WelcomeTest(TestCase):
    def setUp(self) -> None:
        self.__bot_controller = FakeBotController()
        self.__data_service = FakeDataService()
        self.__room_state = RoomState.get_instance(self.__bot_controller)
        self.__welcome = WelcomeCommandProcessor(self.__bot_controller, self.__room_state, self.__data_service)
        self.__mod = create_random_string()
        self.__nonmod = create_random_string()
        self.__room_state.set_mod_ids([self.__mod])
        self.__curly = create_random_string()
        self.__joe = create_random_string()

    def test_mod_user_flow(self) -> None:
        self.__welcome.process(self.__mod)
        self.__dequeue_and_assert_chats([
            'The welcome message is not currently set. To set one, type `/welcome [message]`.'
        ])
        self.__welcome.process(self.__mod, 'foobar')
        self.__dequeue_and_assert_chats([
            'The welcome message has been set to: "foobar"'
        ])
        self.__welcome.process(self.__mod)
        self.__dequeue_and_assert_chats([
            'The current welcome message is: "foobar"'
        ])

    def test_nonmod_user_flow(self) -> None:
        self.__welcome.process(self.__nonmod)
        self.__dequeue_and_assert_chats(['The welcome message is not currently set.'])
        self.__data_service.set_welcome_message('foobar')
        self.__welcome.process(self.__nonmod)
        self.__dequeue_and_assert_chats(['The current welcome message is: "foobar"'])
        self.__welcome.process(self.__nonmod, 'fizzbuzz')
        self.__dequeue_and_assert_chats(['Only mods can update the welcome message!'])
        self.__welcome.process(self.__nonmod)
        self.__dequeue_and_assert_chats(['The current welcome message is: "foobar"'])

    def __dequeue_and_assert_chats(self, expected_chats: List[str]) -> None:
        chats = self.__bot_controller.dequeue_chats()
        self.assertEqual(expected_chats, chats)
