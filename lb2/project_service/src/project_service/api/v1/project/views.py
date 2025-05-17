from typing import List

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

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


@project_router.post("/", response_model=Project)
def create_project_route(
    project_data: ProjectCreate, current_user=Depends(get_current_active_user)
):
    logger.info(f'msg="Logged user" user={current_user}')
    return create_project(project_data)


@project_router.get("/", response_model=List[Project])
def list_projects(current_user=Depends(get_current_active_user)):
    logger.info(f'msg="Logged user" user={current_user}')
    return get_projects()


@project_router.get("/{project_id}", response_model=Project)
def get_project(
    project_id: int,
    current_user=Depends(get_current_active_user),
):
    logger.info(f'msg="Logged user" user={current_user}')
    project = get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@project_router.put("/{project_id}", response_model=Project)
def update_project_route(
    project_id: int,
    project_data: ProjectCreate,
    current_user=Depends(get_current_active_user),
):
    logger.info(f'msg="Logged user" user={current_user}')
    project = update_project(project_id, project_data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@project_router.delete("/{project_id}")
def delete_project_route(
    project_id: int, current_user=Depends(get_current_active_user)
):
    logger.info(f'msg="Logged user" user={current_user}')
    success = delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": "Project deleted"}
