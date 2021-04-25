from abc import ABC, abstractmethod

from dotenv import load_dotenv
from os import environ

load_dotenv()


class AbstractEnvironment(ABC):

    @abstractmethod
    def get_spotify_user_id(self) -> str:
        pass

    @abstractmethod
    def get_jqbx_room_id(self) -> str:
        pass

    @abstractmethod
    def get_jqbx_bot_display_name(self) -> str:
        pass

    @abstractmethod
    def get_jqbx_bot_image_url(self) -> str:
        pass

    @abstractmethod
    def get_data_service_base_url(self) -> str:
        pass


class Environment(AbstractEnvironment):
    def get_spotify_user_id(self) -> str:
        return environ.get('SPOTIFY_USER_ID')

    def get_jqbx_room_id(self) -> str:
        return environ.get('JQBX_ROOM_ID')

    def get_jqbx_bot_display_name(self) -> str:
        return environ.get('JQBX_BOT_DISPLAY_NAME')

    def get_jqbx_bot_image_url(self) -> str:
        return environ.get('JQBX_BOT_IMAGE_URL')

    def get_data_service_base_url(self) -> str:
        return environ.get('DATA_SERVICE_BASE_URL')
