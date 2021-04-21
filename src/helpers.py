from src.constants import bot_user_id
from src.env import AbstractEnvironment


def get_bot_user(env: AbstractEnvironment) -> dict:
    return {
        'username': env.get_jqbx_bot_display_name(),
        'id': bot_user_id,
        'uri': 'spotify:user:%s' % bot_user_id,
        'device': 'bot',
        'status': 'active',
        'country': 'US',
        'image': env.get_jqbx_bot_image_url()
    }
