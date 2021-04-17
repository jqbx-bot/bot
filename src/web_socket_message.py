from typing import Optional


class WebSocketMessage:
    def __init__(self, code: int, label: Optional[str] = None, payload: Optional[dict] = None):
        self.__code = code
        self.__label = label
        self.__payload = payload

    @property
    def code(self) -> int:
        return self.__code

    @property
    def label(self) -> Optional[str]:
        return self.__label

    @property
    def payload(self) -> Optional[dict]:
        return self.__payload
