import traceback

from src.env import AbstractEnvironment, Environment
from src.helpers import get_bot_user
from src.web_socket_client import AbstractWebSocketClient, WebSocketClient
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.web_socket_message_handlers import web_socket_message_handler_map


def main(web_socket_client: AbstractWebSocketClient, env: AbstractEnvironment):
    def __on_open() -> None:
        web_socket_client.send(WebSocketMessage(label='join', payload={
            'roomId': env.get_jqbx_room_id(),
            'user': get_bot_user(env)
        }))

    def __on_message(message: WebSocketMessage) -> None:
        handler = web_socket_message_handler_map.get(message.label, None)
        if handler:
            try:
                handler.handle(message)
            except:
                print(traceback.format_exc())

    web_socket_client.register(__on_open, __on_message)
    web_socket_client.run()


if __name__ == '__main__':
    main(WebSocketClient.get_instance(), Environment())
