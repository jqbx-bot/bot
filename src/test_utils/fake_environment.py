from src.env import AbstractEnvironment


class FakeEnvironment(AbstractEnvironment):
    def get_spotify_user_id(self) -> str:
        return 'spotify_user_id'

    def get_jqbx_bot_display_name(self) -> str:
        return 'jqbx_bot_display_name'

    def get_jqbx_room_id(self) -> str:
        return 'jqbx_room_id'

    def get_jqbx_bot_image_url(self) -> str:
        return 'jqbx_bot_image_url'

    def get_spotify_client_id(self) -> str:
        return 'spotify_client_id'

    def get_spotify_client_secret(self) -> str:
        return 'spotify_client_secret'

    def get_spotify_redirect_uri(self) -> str:
        return 'get_spotify_redirect_uri'

    def get_spotify_refresh_token(self) -> str:
        return 'spotify_refresh_token'
