from typing import List
from unittest import TestCase

from src.command_processors.ro import RockOutCommandProcessor
from src.test_utils.fake_bot import FakeBot
from src.test_utils.test_helpers import create_random_id_object, create_random_string


class RoTest(TestCase):
    def setUp(self) -> None:
        self.__bot = FakeBot()
        self.__ro = RockOutCommandProcessor()
        self.__bot.set_current_track(create_random_id_object())
        self.__mo = create_random_string()
        self.__curly = create_random_string()
        self.__joe = create_random_string()

    def test_ro(self) -> None:
        self.__do_ro(self.__mo)
        self.__dequeue_and_assert_chats([
            'row'
        ])

    def test_ro_twice_same_user(self) -> None:
        self.__do_ro(self.__mo)
        self.__do_ro(self.__mo)
        self.__dequeue_and_assert_chats([
            'row'
        ])
        self.assertFalse(self.__bot.doped)

    def test_ro_two_different_songs(self) -> None:
        self.__do_ro(self.__mo)
        self.__bot.set_current_track(create_random_id_object())
        self.__do_ro(self.__mo)
        self.__dequeue_and_assert_chats([
            'row',
            'row'
        ])
        self.assertFalse(self.__bot.doped)

    def test_ro_ro(self) -> None:
        self.__do_ro(self.__mo)
        self.__do_ro(self.__curly)
        self.__dequeue_and_assert_chats([
            'row',
            'row, row'
        ])
        self.assertFalse(self.__bot.doped)

    def test_ro_ro_ro(self) -> None:
        self.__do_ro(self.__mo)
        self.__do_ro(self.__curly)
        self.__do_ro(self.__joe)
        self.__dequeue_and_assert_chats([
            'row',
            'row, row',
            'row, row, row your :canoe: gently down the stream'
        ])
        self.assertTrue(self.__bot.doped)

    def __do_ro(self, user_id: str) -> None:
        self.__ro.process(self.__bot, user_id)

    def __dequeue_and_assert_chats(self, expected_chats: List[str]) -> None:
        chats = self.__bot.dequeue_chats()
        self.assertEqual(expected_chats, chats)
