from typing import Optional, Union


class WebSocketMessage:
    def __init__(self, code: int = 42, label: Optional[str] = None, payload: Optional[dict] = None):
        self.__code = code
        self.__label = label
        self.__payload = payload
        self.__room_id = self.__detect_room_id(payload) or payload.get('_id') if payload else None

    @property
    def code(self) -> int:
        return self.__code

    @property
    def label(self) -> Optional[str]:
        return self.__label

    @property
    def payload(self) -> Optional[dict]:
        return self.__payload

    @property
    def room_id(self) -> Optional[str]:
        return self.__room_id

    def as_dict(self) -> dict:
        return {
            'room_id': self.__room_id,
            'code': self.__code,
            'label': self.__label,
            'payload': self.payload
        }

    @staticmethod
    def __detect_room_id(search_me: Union[dict, list]) -> Optional[str]:
        if isinstance(search_me, dict) and search_me:
            for key, value in search_me.items():
                if key == 'room':
                    return value
                recursive_search_result = WebSocketMessage.__detect_room_id(search_me[key])
                if recursive_search_result is not None:
                    return recursive_search_result
        elif isinstance(search_me, list) and search_me:
            for item in search_me:
                recursive_search_result = WebSocketMessage.__detect_room_id(item)
                if recursive_search_result is not None:
                    return recursive_search_result
