from typing import List, Dict, Any, Optional

from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "projects_db"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

projects_collection = db["projects"]
tasks_collection = db["tasks"]

projects_collection.create_index("name", unique=True)
projects_collection.create_index("code", unique=True)
tasks_collection.create_index("code", unique=True)


def search_projects_by_name(name: str) -> List[Dict[str, Any]]:
    """Ищет проекты по имени (регистронезависимо)"""
    try:
        projects = list(projects_collection.find(
            {"name": {"$regex": name, "$options": "i"}},
            {"_id": 0, "id": "$_id"}
        ))
        return projects
    except Exception as e:
        print(f"Ошибка при поиске проектов: {str(e)}")
        return []


def get_all_projects() -> List[Dict[str, Any]]:
    """Возвращает все проекты"""
    try:
        projects = list(projects_collection.find(
            {},
            {"_id": 0, "id": "$_id"}
        ))
        return projects
    except Exception as e:
        print(f"Ошибка при получении проектов: {str(e)}")
        return []


def get_all_tasks_in_project(project_id: str) -> List[Dict[str, Any]]:
    """Возвращает все задачи в проекте"""
    try:
        tasks = list(tasks_collection.find(
            {"project_id": project_id},
            {"_id": 0, "id": "$_id"}
        ))
        return tasks
    except Exception as e:
        print(f"Ошибка при получении задач: {str(e)}")
        return []


def get_task_by_code(code: str) -> Optional[Dict[str, Any]]:
    """Находит задачу по коду"""
    try:
        task = tasks_collection.find_one(
            {"code": code},
            {"_id": 0, "id": "$_id"}
        )
        return task
    except Exception as e:
        print(f"Ошибка при поиске задачи: {str(e)}")
        return None
