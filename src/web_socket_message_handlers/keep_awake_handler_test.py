from unittest import TestCase

from src.test_utils.fake_environment import FakeEnvironment
from src.test_utils.fake_web_socket_client import FakeWebSocketClient
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.keep_awake_handler import KeepAwakeHandler


class KeepAwakeHandlerTest(TestCase):
    def setUp(self) -> None:
        self.__env = FakeEnvironment()
        self.__client = FakeWebSocketClient()
        self.__handler = KeepAwakeHandler(self.__client)

    def test_keep_awake(self):
        date = 123
        keep_awake_message = WebSocketMessage(label='keepAwake', payload={'date': date})
        self.__handler.handle(keep_awake_message)
        client_messages = self.__client.dequeue_client_messages()
        stay_awake_message = next(x for x in client_messages if x.label == 'stayAwake')
        self.assertEqual(stay_awake_message.payload['date'], date)
        code_2_message = next(x for x in client_messages if x.code == 2)
        self.assertIsNone(code_2_message.label)
        self.assertIsNone(code_2_message.payload)
