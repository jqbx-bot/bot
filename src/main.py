from src.bot_state import BotState
from src.env import Environment
from src.bot import Bot

if __name__ == '__main__':
    Bot(env=Environment(), state=BotState()).run()
