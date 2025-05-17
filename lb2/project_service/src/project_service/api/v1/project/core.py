from typing import List, Optional

from .models import Project, ProjectCreate

projects_db = []
current_id = 1


def create_project(project_data: ProjectCreate) -> Project:
    global current_id
    project = Project(id=current_id, **project_data.dict())
    projects_db.append(project)
    current_id += 1
    return project


def get_projects() -> List[Project]:
    return projects_db


def get_project_by_id(project_id: int) -> Optional[Project]:
    for project in projects_db:
        if project.id == project_id:
            return project
    return None


def update_project(project_id: int, project_data: ProjectCreate) -> Optional[Project]:
    project = get_project_by_id(project_id)
    if project:
        project.name = project_data.name
        project.description = project_data.description
        return project
    return None


def delete_project(project_id: int) -> bool:
    global projects_db
    initial_length = len(projects_db)
    projects_db = [p for p in projects_db if p.id != project_id]
    return len(projects_db) < initial_length
