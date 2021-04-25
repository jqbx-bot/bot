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

    def get_data_service_base_url(self) -> str:
        return 'data_service_base_url'
