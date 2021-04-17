import random
import string


def create_random_string(size: int = 10) -> str:
    return ''.join(str(random.choice(string.ascii_letters)) for _ in range(size))


def create_random_id_object() -> dict:
    return {'id': create_random_string()}
