from typing import List, Optional

from asyncpg import Pool
from asyncpg.exceptions import UniqueViolationError
from fastapi import HTTPException
from loguru import logger

from ....external.postgres.utils import (
    create_project_in_db,
    delete_project_from_db,
    get_all_projects_from_db,
    get_project_by_id_from_db,
    update_project_in_db,
)
from .models import Project, ProjectCreate


async def create_project(pool: Pool, project_data: ProjectCreate):
    try:
        await create_project_in_db(pool, project_data)
    except UniqueViolationError:
        logger.error(
            f'msg="Tried to create existing project" project_data={project_data}'
        )
        raise HTTPException(status_code=409, detail="Conflict")


async def get_projects(pool: Pool) -> List[Project]:
    return await get_all_projects_from_db(pool)


async def get_project_by_id(pool: Pool, project_id: int) -> Optional[Project]:
    return await get_project_by_id_from_db(pool, project_id)


async def update_project(pool: Pool, project_id: int, project_data: ProjectCreate):
    project = await get_project_by_id_from_db(pool, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Not found project")
    await update_project_in_db(pool, project_id, project_data)


async def delete_project(pool: Pool, project_id: int):
    project = await get_project_by_id_from_db(pool, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Not found project")
    await delete_project_from_db(pool, project_id)
