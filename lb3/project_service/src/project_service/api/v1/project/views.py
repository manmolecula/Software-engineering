from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from loguru import logger

from ....external.postgres.connection import get_connection_pool
from .auth import get_current_active_user
from .core import (
    create_project,
    delete_project,
    get_project_by_id,
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
    pool=Depends(get_connection_pool),
):
    logger.info(f'msg="Logged user" user={current_user}')
    await create_project(pool, project_data)
    response.status_code = 201
    return {"detail": "created"}


@project_router.get("/")
async def list_projects(
    current_user=Depends(get_current_active_user), pool=Depends(get_connection_pool)
):
    logger.info(f'msg="Logged user" user={current_user}')
    return await get_projects(pool)


@project_router.get("/{project_id}")
async def get_project(
    project_id: int,
    current_user=Depends(get_current_active_user),
    pool=Depends(get_connection_pool),
):
    logger.info(f'msg="Logged user" user={current_user}')
    project = await get_project_by_id(pool, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@project_router.put("/{project_id}")
async def update_project_route(
    project_id: int,
    project_data: ProjectCreate,
    current_user=Depends(get_current_active_user),
    pool=Depends(get_connection_pool),
):
    logger.info(f'msg="Logged user" user={current_user}')
    await update_project(pool, project_id, project_data)


@project_router.delete("/{project_id}")
async def delete_project_route(
    project_id: int,
    current_user=Depends(get_current_active_user),
    pool=Depends(get_connection_pool),
):
    logger.info(f'msg="Logged user" user={current_user}')
    await delete_project(pool, project_id)
    return {"detail": "Project deleted"}
