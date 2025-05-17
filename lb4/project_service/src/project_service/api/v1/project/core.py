from typing import List, Optional

from asyncpg import Pool
from asyncpg.exceptions import UniqueViolationError
from fastapi import HTTPException
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorDatabase

from ....external.mongo.utils import (
    create_project_in_db,
    delete_project_from_db,
    get_all_projects_from_db,
    get_project_by_name_from_db,
    update_project_in_db,
)
from .models import Project, ProjectCreate


async def create_project(db: AsyncIOMotorDatabase, project_data: ProjectCreate):
    project = await get_project_by_name_from_db(db, project_data.name)
    if project:
        raise HTTPException(status_code=409, detail="Conflict")
    await create_project_in_db(db, project_data)


async def get_projects(db: AsyncIOMotorDatabase) -> List[Project]:
    return await get_all_projects_from_db(db)


async def get_project_by_name(
    db: AsyncIOMotorDatabase, project_name: str
) -> Optional[Project]:
    return await get_project_by_name_from_db(db, project_name)


async def update_project(
    db: AsyncIOMotorDatabase, project_name: str, project_data: ProjectCreate
):
    project = await get_project_by_name_from_db(db, project_name)
    if not project:
        raise HTTPException(status_code=404, detail="Not found project")
    project = await get_project_by_name_from_db(db, project_data.name)
    if project and project_name != project_data.name:
        raise HTTPException(status_code=409, detail="Conflict")
    await update_project_in_db(db, project_name, project_data)


async def delete_project(db: AsyncIOMotorDatabase, project_name: str):
    project = await get_project_by_name_from_db(db, project_name)
    if not project:
        raise HTTPException(status_code=404, detail="Not found project")
    await delete_project_from_db(db, project_name)
