from typing import Tuple


def encode(text: str) -> Tuple[str]:
    return tuple(map("{:08b}".format, text.encode()))


def decode(data: Tuple[str]) -> str:
    return bytearray([int(_, 2) for _ in data]).decode()
