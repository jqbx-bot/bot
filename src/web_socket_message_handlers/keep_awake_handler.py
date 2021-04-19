from src.web_socket_client import AbstractWebSocketClient, WebSocketClient
from src.web_socket_message import WebSocketMessage
from src.web_socket_message_handlers.abstract_web_socket_message_handler import AbstractWebSocketMessageHandler


class KeepAwakeHandler(AbstractWebSocketMessageHandler):
    def __init__(self, web_socket_client: AbstractWebSocketClient = WebSocketClient.get_instance()):
        self.__web_socket_client = web_socket_client

    @property
    def message_label(self) -> str:
        return 'keepAwake'

    def handle(self, message: WebSocketMessage) -> None:
        self.__web_socket_client.send(WebSocketMessage(label='stayAwake', payload={'date': message.payload['date']}))
        self.__web_socket_client.send(WebSocketMessage(2))
