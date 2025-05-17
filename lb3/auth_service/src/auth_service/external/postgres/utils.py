from typing import Optional

from ...api.v1.auth.models import UserInDB
from .connection import get_connection_pool


async def get_user_from_db(username: str) -> Optional[UserInDB]:
    pool = get_connection_pool()
    query = """
            SELECT *
            FROM users WHERE username = $1
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            row = await connection.fetchrow(query, username)
            if not row:
                return None
            data = dict(**row)
            data["password"] = ""
            return UserInDB(**data)


async def get_users_from_db() -> list[UserInDB]:
    pool = get_connection_pool()
    query = """
            SELECT *
            FROM users
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            rows = await connection.fetch(query)
            res = []
            for row in rows:
                data = dict(**row)
                data["password"] = ""
                res.append(data)
            return [UserInDB(**r) for r in res]


async def get_user_id_from_db(username: str) -> Optional[int]:
    pool = get_connection_pool()
    query = """
            SELECT id
            FROM users WHERE username = $1
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            row = await connection.fetchrow(query, username)
            if not row:
                return None
            return row["id"]


async def create_user(new_user: UserInDB):
    pool = get_connection_pool()
    query = """
            INSERT INTO users (hashed_password, username, initials, role)
            VALUES ($1, $2, $3, $4)
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.fetch(
                query,
                new_user.hashed_password,
                new_user.username,
                new_user.initials,
                new_user.role,
            )


async def save_file_to_db(file_path: str, user_id: int):
    pool = get_connection_pool()
    query = """
            INSERT INTO files (file_path, user_id)
            VALUES ($1, $2)
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.fetch(query, file_path, user_id)


async def delete_user_from_db(id: int):
    pool = get_connection_pool()
    query = """
            DELETE FROM users WHERE id = $1
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(query, id)
