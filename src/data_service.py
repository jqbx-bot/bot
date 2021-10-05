from abc import ABC, abstractmethod
from typing import Optional, Dict, List

import requests

from src.env import AbstractEnvironment, Environment


class AbstractDataService(ABC):
    @abstractmethod
    def get_welcome_message(self) -> Optional[str]:
        pass

    @abstractmethod
    def set_welcome_message(self, welcome_message: str) -> None:
        pass

    @abstractmethod
    def clear_welcome_message(self) -> None:
        pass

    @abstractmethod
    def relink(self, track_id: str, markets: List[str]) -> Optional[Dict[str, str]]:
        pass

    @abstractmethod
    def add_to_favorites_playlist(self, track_id: str) -> Optional[str]:
        pass


class DataService(AbstractDataService):
    def __init__(self, env: AbstractEnvironment = Environment()):
        self.__base_url = env.get_data_service_base_url()
        self.__room_id = env.get_jqbx_room_id()
        self.__cached_welcome_message: Optional[str] = None

    def get_welcome_message(self) -> Optional[str]:
        if self.__cached_welcome_message:
            return self.__cached_welcome_message
        response = requests.get(self.__get_welcome_message_endpoint())
        if response.status_code == 404:
            return None
        return response.json().get('welcome_message')

    def set_welcome_message(self, welcome_message: str) -> None:
        requests.post(self.__get_welcome_message_endpoint(), json={'welcome_message': welcome_message})
        self.__cached_welcome_message = welcome_message

    def clear_welcome_message(self) -> None:
        requests.delete(self.__get_welcome_message_endpoint())
        self.__cached_welcome_message = None

    def relink(self, track_id: str, markets: List[str]) -> Optional[Dict[str, str]]:
        response = requests.get(
            '%s/spotify/relink/%s' % (self.__base_url, track_id),
            params={'markets': ','.join(markets)}
        )
        if response.status_code != 200:
            return None
        return response.json()

    def add_to_favorites_playlist(self, track_id: str) -> Optional[str]:
        response = requests.post('%s/spotify/favorite/%s/%s' % (self.__base_url, self.__room_id, track_id))
        return response.json().get('playlist_id')

    def __get_welcome_message_endpoint(self) -> str:
        return '%s/welcome_message/%s' % (self.__base_url, self.__room_id)
