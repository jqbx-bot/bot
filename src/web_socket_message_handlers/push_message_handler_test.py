from unittest import TestCase

from src.test_utils.fake_command_processor import FakeCommandProcessor
from src.test_utils.fake_environment import FakeEnvironment
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.push_message_handler import PushMessageHandler


class PushMessageHandlerTest(TestCase):
    def setUp(self) -> None:
        self.__env = FakeEnvironment()
        self.__command_processor = FakeCommandProcessor()
        self.__handler = PushMessageHandler(self.__env, [self.__command_processor])

    def test_command(self) -> None:
        self.__handler.handle(WebSocketMessage(
            label='push-message',
            payload=self.__create_push_message('joe', '/fake foo bar')
        ))
        self.assertTrue(self.__command_processor.was_called)
        self.assertEqual(self.__command_processor.call_user_id, 'joe')
        self.assertEqual(self.__command_processor.call_payload, 'foo bar')

    def test_command_no_payload(self) -> None:
        self.__handler.handle(WebSocketMessage(
            label='push-message',
            payload=self.__create_push_message('joe', '/fake ')
        ))
        self.assertTrue(self.__command_processor.was_called)
        self.assertEqual(self.__command_processor.call_user_id, 'joe')
        self.assertIsNone(self.__command_processor.call_payload)

    def test_no_command_because_sent_from_bot(self) -> None:
        self.__handler.handle(WebSocketMessage(
            label='push-message',
            payload=self.__create_push_message(self.__env.get_spotify_user_id(), '/fake foo bar')
        ))
        self.assertFalse(self.__command_processor.was_called)

    def test_no_command_because_malformed(self) -> None:
        self.__handler.handle(WebSocketMessage(
            label='push-message',
            payload=self.__create_push_message('joe', 'fake foo bar')
        ))
        self.assertFalse(self.__command_processor.was_called)

    @staticmethod
    def __create_push_message(user_id: str, message: str) -> dict:
        return {
            'user': {
                'id': user_id
            },
            'message': message
        }