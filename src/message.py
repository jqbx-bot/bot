import json
from typing import Optional


class Message:
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

    @staticmethod
    def parse(raw_message: str) -> 'Message':
        stripped = raw_message.strip()
        parts = stripped.split('[', 1)
        label = None
        payload = None
        if len(parts) > 1:
            json_array = json.loads('[%s' % parts[1])
            label = json_array[0]
            payload = None if len(json_array) == 1 else json_array[1]
        return Message(int(parts[0]), label, payload)
