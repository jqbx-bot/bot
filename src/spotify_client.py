from abc import ABC, abstractmethod
from operator import itemgetter
from typing import Callable, Optional, List

import spotipy
from src.env import AbstractEnvironment, Environment


class AbstractSpotifyClient(ABC):
    @abstractmethod
    def add_to_playlist_and_get_playlist_id(self, playlist_name: str, playlist_description: str, track_id: str,
                                            n_to_keep: int) -> str:
        pass


class SpotifyClient(AbstractSpotifyClient):
    __instance: Optional['SpotifyClient'] = None

    def __init__(self, env: AbstractEnvironment = Environment()):
        if SpotifyClient.__instance:
            raise Exception('Use get_instance() instead!')
        self.__env = env
        self.__oauth: Optional[spotipy.oauth2.SpotifyOAuth] = None
        self.__token_info: Optional[dict] = None
        SpotifyClient.__instance = self

    @staticmethod
    def get_instance() -> 'SpotifyClient':
        if SpotifyClient.__instance is None:
            SpotifyClient()
        return SpotifyClient.__instance

    def add_to_playlist_and_get_playlist_id(self, playlist_name: str, playlist_description: str, track_id: str,
                                            n_to_keep: int) -> str:
        client = self.__get_authenticated_client()
        playlist_id = self.__get_or_create_playlist(client, playlist_name)
        client.playlist_change_details(playlist_id, description=playlist_description)
        client.playlist_remove_all_occurrences_of_items(playlist_id, [track_id])
        client.playlist_add_items(playlist_id, [track_id], 0)
        tracks: List[dict] = client.playlist_items(playlist_id, limit=n_to_keep)['items']
        client.playlist_replace_items(playlist_id, [x['track']['id'] for x in tracks])
        return playlist_id

    def __get_or_create_playlist(self, client: spotipy.Spotify, playlist_name: str) -> str:
        playlists = self.__get_paginated_items(lambda offset: client.current_user_playlists(offset=offset))
        playlist = next((p for p in playlists if p['name'] == playlist_name), None)
        if playlist:
            return playlist['id']
        playlist_id = client.user_playlist_create(self.__env.get_spotify_user_id(), playlist_name)['id']
        return playlist_id

    def __get_authenticated_client(self) -> spotipy.Spotify:
        if not self.__oauth:
            self.__oauth = spotipy.oauth2.SpotifyOAuth(
                client_id=self.__env.get_spotify_client_id(),
                client_secret=self.__env.get_spotify_client_secret(),
                redirect_uri=self.__env.get_spotify_redirect_uri()
            )
        if not self.__token_info or self.__oauth.is_token_expired(self.__token_info):
            self.__token_info = self.__oauth.refresh_access_token(self.__env.get_spotify_refresh_token())
        return spotipy.Spotify(auth=self.__token_info['access_token'])

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
