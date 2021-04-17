from unittest import TestCase

from src.bot import Bot
from src.bot_state import BotState
from src.test_utils.fake_environment import FakeEnvironment
from src.test_utils.fake_web_socket_client import FakeWebSocketClient
from src.web_socket_message import WebSocketMessage


class BotTest(TestCase):
    def setUp(self) -> None:
        self.__env = FakeEnvironment()
        self.__client = FakeWebSocketClient()
        self.__state = BotState()
        bot = Bot(self.__env, self.__state, self.__client, [])
        bot.run()

    def test_join(self):
        join_message = next(x for x in self.__client.dequeue_client_messages() if x.label == 'join')
        self.assertEqual(join_message.payload['roomId'], self.__env.get_jqbx_room_id())
        self.assertEqual(join_message.payload['user']['id'], self.__env.get_spotify_user_id())

    def test_keep_awake(self):
        date = 123
        keep_awake_message = WebSocketMessage(42, 'keepAwake', {'date': date})
        self.__client.send_server_message(keep_awake_message)
        stay_awake_message = next(x for x in self.__client.dequeue_client_messages() if x.label == 'stayAwake')
        self.assertEqual(stay_awake_message.payload['date'], date)

    def test_room_update_mod_ids(self):
        self.assertEqual(len(self.__state.mod_ids), 0)

        room_update_message = WebSocketMessage(42, 'update-room', {
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

        self.assertEqual(len(self.__state.mod_ids), 3)
        self.assertTrue('1' in self.__state.mod_ids)
        self.assertTrue('2' in self.__state.mod_ids)
        self.assertTrue('3' in self.__state.mod_ids)

    def test_room_update_welcome(self):
        self.__state.set_welcome_message('what it do nephew')
        self.__state.set_user_ids(['1', '2'])
        self.__client.send_server_message(WebSocketMessage(42, 'update-room', {
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
        self.assertEqual(len(self.__state.user_ids), 4)

    def test_room_update_no_welcome_because_no_initial_users(self):
        self.__state.set_welcome_message('what it do nephew')
        self.__client.send_server_message(WebSocketMessage(42, 'update-room', {
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
        self.__state.set_user_ids(['a'])
        self.__client.send_server_message(WebSocketMessage(42, 'update-room', {
            'admin': [],
            'mods': [],
            'users': [
                self.__to_spotify_user('a'),
                self.__to_spotify_user('b')
            ]
        }))
        chat_messages = [x for x in self.__client.dequeue_client_messages() if x.label == 'chat']
        self.assertEqual(len(chat_messages), 0)

    @staticmethod
    def __to_spotify_uri(user_id: str) -> str:
        return 'spotify:user:%s' % user_id

    @staticmethod
    def __to_spotify_user(user_id: str) -> dict:
        return {
            'id': user_id,
            'username': 'User%s' % user_id
        }
