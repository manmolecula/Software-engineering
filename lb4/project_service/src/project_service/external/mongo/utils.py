from typing import Union

from motor.motor_asyncio import AsyncIOMotorDatabase

from ...api.v1.project.models import Project, ProjectCreate
from ...settings import settings


async def get_project_by_name_from_db(
    db: AsyncIOMotorDatabase, name: str
) -> Union[Project, None]:
    project = await db[settings.mongo_collection].find_one({"name": name})
    return Project(**project) if project else None


async def get_all_projects_from_db(db: AsyncIOMotorDatabase) -> list[Project]:
    projects = await db[settings.mongo_collection].find().to_list()
    print(projects)
    return [Project(**project) for project in projects]


async def create_project_in_db(db: AsyncIOMotorDatabase, project: ProjectCreate):
    await db[settings.mongo_collection].insert_one(project.model_dump())


async def delete_project_from_db(db: AsyncIOMotorDatabase, name: str):
    await db[settings.mongo_collection].delete_one({"name": name})


async def update_project_in_db(
    db: AsyncIOMotorDatabase, name: str, project: ProjectCreate
):
    await db[settings.mongo_collection].update_one(
        {"name": name}, {"$set": project.model_dump()}
    )
