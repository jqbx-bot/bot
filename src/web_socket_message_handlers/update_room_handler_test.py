import copy
from typing import List
from unittest import TestCase

from src.room_state import RoomState
from src.test_utils.fake_bot_controller import FakeBotController
from src.test_utils.test_helpers import create_random_id_object
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.update_room_handler import UpdateRoomHandler


class UpdateRoomHandlerTest(TestCase):
    def setUp(self) -> None:
        self.__bot_controller = FakeBotController()
        self.__room_state = copy.deepcopy(RoomState.get_instance(self.__bot_controller))
        self.__handler = UpdateRoomHandler(self.__bot_controller, self.__room_state)

    def test_mod_ids(self):
        self.assertEqual(len(self.__room_state.mod_ids), 0)
        room_update_message = WebSocketMessage(label='update-room', payload={
            'admin': [
                self.__to_spotify_uri('1'),
                self.__to_spotify_uri('2')
            ],
            'mods': [
                self.__to_spotify_uri('2'),
                self.__to_spotify_uri('3')
            ]
        })
        self.__handler.handle(room_update_message)
        self.assertEqual(sorted(['1', '2', '3']), sorted(self.__room_state.mod_ids))
        self.__handler.handle(WebSocketMessage(label='update-room', payload={}))
        self.assertEqual(sorted(['1', '2', '3']), sorted(self.__room_state.mod_ids))

    def test_welcome(self):
        self.__bot_controller.set_welcome_message('what it do nephew')
        self.__handler.handle(WebSocketMessage(label='update-room', payload={
            'users': [
                self.__to_spotify_user('1'),
                self.__to_spotify_user('2')
            ]
        }))
        self.__dequeue_and_assert_whispers([])
        self.__handler.handle(WebSocketMessage(label='update-room', payload={
            'users': [
                self.__to_spotify_user('1'),
                self.__to_spotify_user('2'),
                self.__to_spotify_user('3'),
                self.__to_spotify_user('4')
            ]
        }))
        self.__dequeue_and_assert_whispers([
            '@User3 what it do nephew',
            '@User4 what it do nephew'
        ])

    def test_no_welcome_because_no_initial_users(self):
        self.__bot_controller.set_welcome_message('what it do nephew')
        self.__handler.handle(WebSocketMessage(label='update-room', payload={
            'users': [
                self.__to_spotify_user('1'),
                self.__to_spotify_user('2')
            ]
        }))
        self.__dequeue_and_assert_whispers([])

    def test_no_welcome_because_no_message(self):
        self.__handler.handle(WebSocketMessage(label='update-room', payload={
            'users': [
                self.__to_spotify_user('a')
            ]
        }))
        self.__handler.handle(WebSocketMessage(label='update-room', payload={
            'users': [
                self.__to_spotify_user('a'),
                self.__to_spotify_user('b')
            ]
        }))
        self.__dequeue_and_assert_whispers([])

    def test_tracks(self):
        self.assertIsNone(self.__room_state.current_track)
        last_track = create_random_id_object()
        self.__handler.handle(WebSocketMessage(label='update-room', payload={
            'tracks': [
                last_track,
                create_random_id_object()
            ]
        }))
        self.assertEqual(last_track, self.__room_state.current_track)

    def test_room_title(self):
        self.assertIsNone(self.__room_state.room_title)
        self.__handler.handle(WebSocketMessage(label='update-room', payload={
            'title': 'foobar'
        }))
        self.assertEqual('foobar', self.__room_state.room_title)
        self.__handler.handle(WebSocketMessage(label='update-room', payload={}))
        self.assertEqual('foobar', self.__room_state.room_title)

    def __dequeue_and_assert_whispers(self, expected_whispers: List[str]) -> None:
        self.assertEqual(expected_whispers, self.__bot_controller.dequeue_whispers())

    @staticmethod
    def __to_spotify_uri(user_id: str) -> str:
        return 'spotify:user:%s' % user_id

    @staticmethod
    def __to_spotify_user(user_id: str) -> dict:
        return {
            'id': user_id,
            'username': 'User%s' % user_id
        }
