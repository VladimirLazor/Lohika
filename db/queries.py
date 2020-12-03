from contextlib import closing
from sqlite3 import Connection as SqliteConnection
from typing import Dict
from typing import List
from typing import Optional

from .models import Image
from .models import User


def add_user(conn: SqliteConnection,
             user_data: Dict) -> None:
    external_id = user_data.pop('id')
    user_data['external_id'] = external_id

    for field in ('first_name', 'last_name', 'username'):
        value = user_data.get(field)
        if value:
            continue
        user_data[field] = ''

    with closing(conn.cursor()) as cursor:
        cursor.execute("""
            insert into users(external_id, first_name, last_name, username, is_bot)
            select :external_id, :first_name, :last_name, :username, :is_bot
            where not exists(select 1 from users where external_id = :external_id)
        """, user_data)
        conn.commit()


def get_user(conn: SqliteConnection,
             user_id: int) -> Optional[User]:
    with closing(conn.cursor()) as cursor:
        cursor.execute("""
            select *
            from users
            where external_id = :external_id
        """, {'external_id': user_id})
        row = cursor.fetchone()
        return User(**row) if row else None


def delete_user(conn: SqliteConnection,
                user_id: int) -> None:
    with closing(conn.cursor()) as cursor:
        cursor.execute("""
            delete from users where external_id = :external_id
        """, {'external_id': user_id})
        conn.commit()


def add_image(conn: SqliteConnection,
              image_data: Dict) -> None:
    with closing(conn.cursor()) as cursor:
        cursor.execute("""
            insert into images(path, user_id, text)
            select :image_path, :user_id, :text
            where not exists(select 1 from images where user_id = :user_id and path = :image_path)
        """, image_data)
        conn.commit()


def get_images(conn: SqliteConnection,
               user_id: int) -> Optional[List[Image]]:
    with closing(conn.cursor()) as cursor:
        cursor.execute("""
            select *
            from images
            where user_id = :user_id
        """, {'user_id': user_id})
        rows = cursor.fetchall()
        return [Image(**row) for row in rows] if rows else []


def delete_image(conn: SqliteConnection,
                 image_id: int) -> None:
    with closing(conn.cursor()) as cursor:
        cursor.execute("""
            delete from images where id = :image_id
        """, {'image_id': image_id})
        conn.commit()


def get_image(conn: SqliteConnection,
              user_id: int,
              image_id: int) -> Optional[Image]:
    with closing(conn.cursor()) as cursor:
        cursor.execute("""
            select *
            from images
            where user_id = :user_id and id = :image_id
        """, {'user_id': user_id, 'image_id': image_id})

        row = cursor.fetchone()
        return Image(**row) if row else None
