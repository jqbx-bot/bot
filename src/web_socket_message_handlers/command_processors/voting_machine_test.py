from typing import List
from unittest import TestCase

from src.room_state import RoomState
from src.test_utils.fake_bot_controller import FakeBotController
from src.test_utils.test_helpers import create_random_id_object, create_random_string
from src.web_socket_message_handlers.command_processors.voting_machine import VotingMachine


class VotingMachineTest(TestCase):
    def setUp(self) -> None:
        self.__bot_controller = FakeBotController()
        self.__room_state = RoomState.get_instance(self.__bot_controller)
        self.__voting_machine = VotingMachine('row', 'row, row, row your :canoe: gently down the stream',
                                              self.__bot_controller, self.__room_state)
        self.__room_state.set_current_track(create_random_id_object())
        self.__mo = create_random_string()
        self.__curly = create_random_string()
        self.__joe = create_random_string()

    def test_ro(self) -> None:
        self.__do_vote(self.__mo)
        self.__dequeue_and_assert_chats([
            'row'
        ])

    def test_ro_twice_same_user(self) -> None:
        self.__do_vote(self.__mo)
        self.__do_vote(self.__mo)
        self.__dequeue_and_assert_chats([
            'row',
            'You\'ve already voted'
        ])
        self.assertFalse(self.__bot_controller.doped)

    def test_ro_two_different_songs(self) -> None:
        self.__do_vote(self.__mo)
        self.__room_state.set_current_track(create_random_id_object())
        self.__do_vote(self.__mo)
        self.__dequeue_and_assert_chats([
            'row',
            'row'
        ])
        self.assertFalse(self.__bot_controller.doped)

    def test_ro_ro(self) -> None:
        self.__do_vote(self.__mo)
        self.__do_vote(self.__curly)
        self.__dequeue_and_assert_chats([
            'row',
            'row, row'
        ])
        self.assertFalse(self.__bot_controller.doped)

    def test_ro_ro_ro(self) -> None:
        self.__do_vote(self.__mo)
        self.__do_vote(self.__curly)
        self.__do_vote(self.__joe)
        self.__dequeue_and_assert_chats([
            'row',
            'row, row',
            'row, row, row your :canoe: gently down the stream'
        ])
        self.assertTrue(self.__bot_controller.doped)

    def test_already_bopping(self) -> None:
        self.__bot_controller.dope()
        self.__do_vote(self.__mo)
        self.__dequeue_and_assert_chats([
            'I\'m already bopping to this'
        ])

    def test_already_hating(self) -> None:
        self.__bot_controller.nope()
        self.__do_vote(self.__mo)
        self.__dequeue_and_assert_chats([
            'I\'m already hating this'
        ])

    def __do_vote(self, user_id: str) -> None:
        self.__voting_machine.vote(user_id, lambda x: x.dope())

    def __dequeue_and_assert_chats(self, expected_chats: List[str]) -> None:
        chats = self.__bot_controller.dequeue_chats()
        self.assertEqual(expected_chats, chats)
