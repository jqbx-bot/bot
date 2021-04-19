from abc import ABC, abstractmethod
from operator import itemgetter
from typing import Callable, Optional, List

import spotipy
from src.env import AbstractEnvironment, Environment


class AbstractSpotifyClient(ABC):
    @abstractmethod
    def add_to_playlist_and_get_playlist_id(self, playlist_name: str, track_id: str) -> str:
        pass


class SpotifyClient(AbstractSpotifyClient):
    __instance: Optional['SpotifyClient'] = None

    def __init__(self, env: AbstractEnvironment = Environment()):
        if SpotifyClient.__instance:
            raise Exception('Use get_instance() instead!')
        self.__env = env
        self.__spotipy: spotipy.Spotify = spotipy.Spotify(
            auth=spotipy.oauth2.SpotifyOAuth(
                client_id=env.get_spotify_client_id(),
                client_secret=env.get_spotify_client_secret(),
                redirect_uri=env.get_spotify_redirect_uri()
            ).refresh_access_token(env.get_spotify_refresh_token())['access_token']
        )
        SpotifyClient.__instance = self

    @staticmethod
    def get_instance() -> 'SpotifyClient':
        if SpotifyClient.__instance is None:
            SpotifyClient()
        return SpotifyClient.__instance

    def add_to_playlist_and_get_playlist_id(self, playlist_name: str, track_id: str) -> str:
        playlist_id = self.__get_or_create_playlist(playlist_name)
        self.__spotipy.playlist_remove_all_occurrences_of_items(playlist_id, [track_id])
        self.__spotipy.playlist_add_items(playlist_id, [track_id])
        return playlist_id

    def __get_or_create_playlist(self, playlist_name: str) -> str:
        playlists = self.__get_paginated_items(lambda offset: self.__spotipy.current_user_playlists(offset=offset))
        playlist = next((p for p in playlists if p['name'] == playlist_name), None)
        if playlist:
            return playlist['id']
        playlist_id = self.__spotipy.user_playlist_create(self.__env.get_spotify_user_id(), playlist_name)['id']
        return playlist_id

    @staticmethod
    def __get_paginated_items(get_items_at_offset: Callable, n_to_get: Optional[int] = None) -> List[dict]:
        items = []
        offset = 0
        while True:
            new_items, limit = itemgetter('items', 'limit')(get_items_at_offset(offset))
            if not new_items:
                break
            offset += limit
            items.extend(new_items)
            if n_to_get and len(items) >= n_to_get:
                break
        return items[:n_to_get]
