from typing import List
from unittest import TestCase

from src.command_processors.no import NockOutCommandProcessor
from src.test_utils.fake_bot import FakeBot
from src.test_utils.test_helpers import create_random_id_object, create_random_string


class NoTest(TestCase):
    def setUp(self) -> None:
        self.__bot = FakeBot()
        self.__no = NockOutCommandProcessor()
        self.__bot.set_current_track(create_random_id_object())
        self.__mo = create_random_string()
        self.__curly = create_random_string()
        self.__joe = create_random_string()

    def test_no(self) -> None:
        self.__do_no(self.__mo)
        self.__dequeue_and_assert_chats([
            'no'
        ])

    def test_no_twice_same_user(self) -> None:
        self.__do_no(self.__mo)
        self.__do_no(self.__mo)
        self.__dequeue_and_assert_chats([
            'no',
            'You\'ve already voted'
        ])
        self.assertFalse(self.__bot.noped)

    def test_no_two_different_songs(self) -> None:
        self.__do_no(self.__mo)
        self.__bot.set_current_track(create_random_id_object())
        self.__do_no(self.__mo)
        self.__dequeue_and_assert_chats([
            'no',
            'no'
        ])
        self.assertFalse(self.__bot.noped)

    def test_no_no(self) -> None:
        self.__do_no(self.__mo)
        self.__do_no(self.__curly)
        self.__dequeue_and_assert_chats([
            'no',
            'no, no'
        ])
        self.assertFalse(self.__bot.noped)

    def test_no_no_no(self) -> None:
        self.__do_no(self.__mo)
        self.__do_no(self.__curly)
        self.__do_no(self.__joe)
        self.__dequeue_and_assert_chats([
            'no',
            'no, no',
            'no, no, no :-1: no way José!'
        ])
        self.assertTrue(self.__bot.noped)

    def test_already_bopping(self) -> None:
        self.__bot.dope()
        self.__do_no(self.__mo)
        self.__dequeue_and_assert_chats([
            'I\'m already bopping to this'
        ])

    def test_already_hating(self) -> None:
        self.__bot.nope()
        self.__do_no(self.__mo)
        self.__dequeue_and_assert_chats([
            'I\'m already hating this'
        ])

    def __do_no(self, user_id: str) -> None:
        self.__no.process(self.__bot, user_id)

    def __dequeue_and_assert_chats(self, expected_chats: List[str]) -> None:
        chats = self.__bot.dequeue_chats()
        self.assertEqual(expected_chats, chats)
