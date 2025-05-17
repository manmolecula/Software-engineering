from typing import Union

from asyncpg import Pool

from ...api.v1.project.models import Project, ProjectCreate


async def get_project_by_id_from_db(pool: Pool, id: int) -> Union[Project, None]:
    query = """
            SELECT * FROM projects
            WHERE id = $1 LIMIT 1
            """

    async with pool.acquire() as connection:
        async with connection.transaction():
            row = await connection.fetchrow(query, id)
            return Project(**row) if row else None


async def get_all_projects_from_db(pool: Pool) -> list[Project]:
    query = """
            SELECT * FROM projects
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            rows = await connection.fetch(query)
            return [Project(**row) for row in rows]


async def create_project_in_db(pool: Pool, project: ProjectCreate):
    query = """
            INSERT INTO projects (name, description)
            VALUES ($1, $2)
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(query, project.name, project.description)


async def delete_project_from_db(pool: Pool, id: int):
    query = """
            DELETE FROM projects
            WHERE id = $1
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(query, id)


async def update_project_in_db(pool: Pool, id: int, project: ProjectCreate):
    query = """
            UPDATE projects SET name = $1, description = $2
            WHERE id = $3
            """
    async with pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute(query, project.name, project.description, id)
