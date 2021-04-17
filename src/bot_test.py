from unittest import TestCase

from src.bot import Bot
from src.test_utils.fake_command_processor import FakeCommandProcessor
from src.test_utils.fake_environment import FakeEnvironment
from src.test_utils.fake_web_socket_client import FakeWebSocketClient
from src.web_socket_message import WebSocketMessage


class BotTest(TestCase):
    def setUp(self) -> None:
        self.__env = FakeEnvironment()
        self.__client = FakeWebSocketClient()
        self.__command_processor = FakeCommandProcessor()
        self.__bot = Bot(self.__env, self.__client, [self.__command_processor])
        self.__bot.run()

    def test_join(self):
        join_message = next(x for x in self.__client.dequeue_client_messages() if x.label == 'join')
        self.assertEqual(join_message.payload['roomId'], self.__env.get_jqbx_room_id())
        self.assertEqual(join_message.payload['user']['id'], self.__env.get_spotify_user_id())

    def test_keep_awake(self):
        date = 123
        keep_awake_message = WebSocketMessage(label='keepAwake', payload={'date': date})
        self.__client.send_server_message(keep_awake_message)
        client_messages = self.__client.dequeue_client_messages()
        stay_awake_message = next(x for x in client_messages if x.label == 'stayAwake')
        self.assertEqual(stay_awake_message.payload['date'], date)
        code_2_message = next(x for x in client_messages if x.code == 2)
        self.assertIsNone(code_2_message.label)
        self.assertIsNone(code_2_message.payload)

    def test_room_update_mod_ids(self):
        self.assertEqual(len(self.__bot.mod_ids), 0)

        room_update_message = WebSocketMessage(label='update-room', payload={
            'admin': [
                self.__to_spotify_uri('1'),
                self.__to_spotify_uri('2')
            ],
            'mods': [
                self.__to_spotify_uri('2'),
                self.__to_spotify_uri('3')
            ],
            'users': []
        })
        self.__client.send_server_message(room_update_message)

        self.assertEqual(len(self.__bot.mod_ids), 3)
        self.assertTrue('1' in self.__bot.mod_ids)
        self.assertTrue('2' in self.__bot.mod_ids)
        self.assertTrue('3' in self.__bot.mod_ids)

    def test_room_update_welcome(self):
        self.__bot.set_welcome_message('what it do nephew')
        self.__client.send_server_message(WebSocketMessage(label='update-room', payload={
            'admin': [],
            'mods': [],
            'users': [
                self.__to_spotify_user('1'),
                self.__to_spotify_user('2')
            ]
        }))
        self.__client.send_server_message(WebSocketMessage(label='update-room', payload={
            'admin': [],
            'mods': [],
            'users': [
                self.__to_spotify_user('1'),
                self.__to_spotify_user('2'),
                self.__to_spotify_user('3'),
                self.__to_spotify_user('4')
            ]
        }))
        chat_messages = [x for x in self.__client.dequeue_client_messages() if x.label == 'chat']
        self.assertEqual(len(chat_messages), 2)
        chat_messages = [x.payload['message']['message'] for x in chat_messages]
        self.assertTrue('@User3 what it do nephew' in chat_messages)
        self.assertTrue('@User4 what it do nephew' in chat_messages)

    def test_room_update_no_welcome_because_no_initial_users(self):
        self.__bot.set_welcome_message('what it do nephew')
        self.__client.send_server_message(WebSocketMessage(label='update-room', payload={
            'admin': [],
            'mods': [],
            'users': [
                self.__to_spotify_user('1'),
                self.__to_spotify_user('2')
            ]
        }))
        chat_messages = [x for x in self.__client.dequeue_client_messages() if x.label == 'chat']
        self.assertEqual(len(chat_messages), 0)

    def test_room_update_no_welcome_because_no_message(self):
        self.__client.send_server_message(WebSocketMessage(label='update-room', payload={
            'admin': [],
            'mods': [],
            'users': [
                self.__to_spotify_user('a')
            ]
        }))
        self.__client.send_server_message(WebSocketMessage(label='update-room', payload={
            'admin': [],
            'mods': [],
            'users': [
                self.__to_spotify_user('a'),
                self.__to_spotify_user('b')
            ]
        }))
        chat_messages = [x for x in self.__client.dequeue_client_messages() if x.label == 'chat']
        self.assertEqual(len(chat_messages), 0)

    def test_push_message_command(self) -> None:
        self.__client.send_server_message(WebSocketMessage(
            label='push-message',
            payload=self.__create_push_message('joe', '/fake foo bar')
        ))
        self.assertTrue(self.__command_processor.was_called)
        self.assertEqual(self.__command_processor.call_user_id, 'joe')
        self.assertEqual(self.__command_processor.call_payload, 'foo bar')

    def test_push_message_command_no_payload(self) -> None:
        self.__client.send_server_message(WebSocketMessage(
            label='push-message',
            payload=self.__create_push_message('joe', '/fake ')
        ))
        self.assertTrue(self.__command_processor.was_called)
        self.assertEqual(self.__command_processor.call_user_id, 'joe')
        self.assertIsNone(self.__command_processor.call_payload)

    def test_push_message_no_command_because_sent_from_bot(self) -> None:
        self.__client.send_server_message(WebSocketMessage(
            label='push-message',
            payload=self.__create_push_message(self.__env.get_spotify_user_id(), '/fake foo bar')
        ))
        self.assertFalse(self.__command_processor.was_called)

    def test_push_message_no_command_because_malformed(self) -> None:
        self.__client.send_server_message(WebSocketMessage(
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

    @staticmethod
    def __to_spotify_uri(user_id: str) -> str:
        return 'spotify:user:%s' % user_id

    @staticmethod
    def __to_spotify_user(user_id: str) -> dict:
        return {
            'id': user_id,
            'username': 'User%s' % user_id
        }
