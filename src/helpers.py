from src.env import AbstractEnvironment


def get_bot_user(env: AbstractEnvironment) -> dict:
    return {
        'username': env.get_jqbx_bot_display_name(),
        'id': env.get_spotify_user_id(),
        'uri': 'spotify:user:%s' % env.get_spotify_user_id(),
        'device': 'bot',
        'status': 'active',
        'country': 'US',
        'image': env.get_jqbx_bot_image_url()
    }