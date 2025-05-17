from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from loguru import logger

from ....external.mongo.mongo_db import get_mongo_database
from ....external.postgres.connection import get_connection_pool
from .auth import get_current_active_user
from .core import (
    create_project,
    delete_project,
    get_project_by_name,
    get_projects,
    update_project,
)
from .models import Project, ProjectCreate

project_router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])


@project_router.post("/")
async def create_project_route(
    project_data: ProjectCreate,
    response: Response,
    current_user=Depends(get_current_active_user),
    # pool=Depends(get_connection_pool),
    mongo_db=Depends(get_mongo_database),
):
    logger.info(f'msg="Logged user" user={current_user}')
    await create_project(mongo_db, project_data)
    response.status_code = 201
    return {"detail": "created"}


@project_router.get("/")
async def list_projects(
    current_user=Depends(get_current_active_user),
    # pool=Depends(get_connection_pool),
    mongo_db=Depends(get_mongo_database),
):
    logger.info(f'msg="Logged user" user={current_user}')
    return await get_projects(mongo_db)


@project_router.get("/{project_name}")
async def get_project(
    project_name: str,
    current_user=Depends(get_current_active_user),
    # pool=Depends(get_connection_pool),
    mongo_db=Depends(get_mongo_database),
):
    logger.info(f'msg="Logged user" user={current_user}')
    project = await get_project_by_name(mongo_db, project_name)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@project_router.put("/{project_name}")
async def update_project_route(
    project_name: str,
    project_data: ProjectCreate,
    current_user=Depends(get_current_active_user),
    # pool=Depends(get_connection_pool),
    mongo_db=Depends(get_mongo_database),
):
    logger.info(f'msg="Logged user" user={current_user}')
    await update_project(mongo_db, project_name, project_data)


@project_router.delete("/{project_name}")
async def delete_project_route(
    project_name: str,
    current_user=Depends(get_current_active_user),
    # pool=Depends(get_connection_pool),
    mongo_db=Depends(get_mongo_database),
):
    logger.info(f'msg="Logged user" user={current_user}')
    await delete_project(mongo_db, project_name)
    return {"detail": "Project deleted"}
