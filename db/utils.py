from functools import partial
from functools import wraps
from typing import Callable

sql = """

pragma foreign_keys = on;

create table if not exists users
(
  id                  integer primary key autoincrement,
  external_id         text     not null,
  first_name          text     not null,
  last_name           text     not null,
  username            text     not null,
  is_bot              integer  not null 
);

create table if not exists images
(
  id                  integer primary key autoincrement,
  path                text     not null,
  user_id             integer  not null,
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

create unique index if not exists users_id_uindex
  on users (id);
create unique index if not exists users_external_id_uindex
  on users (external_id);
create unique index if not exists users_username_uindex
  on users (username);

"""


def check_db(db_connect) -> None:
    db_connect.executescript(sql)


def db_cache(func: Callable = None) -> Callable:
    _cache = {}

    if func is None:
        return partial(db_cache)

    @wraps(func)
    def __wrapper(*args, **kwargs):
        *_, _external_id = args
        _id = _cache.get(_external_id)
        if _id is None:
            _id = func(*args, **kwargs)
            if _id is not None:
                _cache[_external_id] = _id
        return _id

    return __wrapper
