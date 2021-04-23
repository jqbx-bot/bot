from abc import ABC, abstractmethod
from typing import Optional

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


class DataService(AbstractDataService):
    def __init__(self, env: AbstractEnvironment = Environment()):
        self.__base_url = env.get_data_service_base_url()
        self.__room_id = env.get_jqbx_room_id()

    def get_welcome_message(self) -> Optional[str]:
        response = requests.get(self.__get_welcome_message_endpoint())
        if response.status_code == 404:
            return None
        return response.json().get('welcome_message')

    def set_welcome_message(self, welcome_message: str) -> None:
        requests.post(self.__get_welcome_message_endpoint(), json={'welcome_message': welcome_message})

    def clear_welcome_message(self) -> None:
        requests.delete(self.__get_welcome_message_endpoint())

    def __get_welcome_message_endpoint(self) -> str:
        return '%s/welcome_message/%s' % (self.__base_url, self.__room_id)