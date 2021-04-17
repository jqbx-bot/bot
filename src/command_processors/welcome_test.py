from typing import List
from unittest import TestCase

from src.command_processors.welcome import WelcomeCommandProcessor
from src.test_utils.fake_bot import FakeBot
from src.test_utils.test_helpers import create_random_string


class WelcomeTest(TestCase):
    def setUp(self) -> None:
        self.__bot = FakeBot()
        self.__mod = create_random_string()
        self.__nonmod = create_random_string()
        self.__welcome = WelcomeCommandProcessor()
        self.__bot.set_mod_ids([self.__mod])
        self.__curly = create_random_string()
        self.__joe = create_random_string()

    def test_mod_user_flow(self) -> None:
        self.__welcome.process(self.__bot, self.__mod)
        self.__dequeue_and_assert_chats([
            'The welcome message is not currently set. To set one, type `/welcome [message]`.'
        ])
        self.__welcome.process(self.__bot, self.__mod, 'foobar')
        self.__dequeue_and_assert_chats([
            'The welcome message has been set to: "foobar"'
        ])
        self.__welcome.process(self.__bot, self.__mod)
        self.__dequeue_and_assert_chats([
            'The current welcome message is: "foobar"'
        ])

    def test_nonmod_user_flow(self) -> None:
        self.__welcome.process(self.__bot, self.__nonmod)
        self.__dequeue_and_assert_chats(['The welcome message is not currently set.'])
        self.__bot.set_welcome_message('foobar')
        self.__welcome.process(self.__bot, self.__nonmod)
        self.__dequeue_and_assert_chats(['The current welcome message is: "foobar"'])
        self.__welcome.process(self.__bot, self.__nonmod, 'fizzbuzz')
        self.__dequeue_and_assert_chats(['Only mods can update the welcome message!'])
        self.__welcome.process(self.__bot, self.__nonmod)
        self.__dequeue_and_assert_chats(['The current welcome message is: "foobar"'])

    def __dequeue_and_assert_chats(self, expected_chats: List[str]) -> None:
        chats = self.__bot.dequeue_chats()
        self.assertEqual(expected_chats, chats)
