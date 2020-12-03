from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    external_id: int
    is_bot: bool
    first_name: str = ''
    last_name: str = ''
    username: str = ''


@dataclass(frozen=True)
class Image:
    id: int
    path: str
    user_id: int
    text: str
