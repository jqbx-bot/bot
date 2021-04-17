from src.bot_state import BotState
from src.command_processors.command_processors import command_processors
from src.env import Environment
from src.bot import Bot
from src.web_socket_client import WebSocketClient

if __name__ == '__main__':
    Bot(
        env=Environment(),
        state=BotState(),
        web_socket_client=WebSocketClient(),
        command_processors=command_processors
    ).run()
