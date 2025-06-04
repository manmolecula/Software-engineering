import uuid
from typing import Dict, Any

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "projects_db"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

projects_collection = db["projects"]
tasks_collection = db["tasks"]

projects_collection.create_index("name", unique=True)
projects_collection.create_index("code", unique=True)
tasks_collection.create_index("code", unique=True)


def create_project(project_data: Dict[str, Any]) -> Dict[str, Any]:
    """Создает новый проект в MongoDB"""
    try:
        project_id = str(uuid.uuid4())
        project_data["_id"] = project_id

        if not project_data.get("code"):
            project_data["code"] = f"PROJ-{project_id[:8]}"

        result = projects_collection.insert_one(project_data)

        if result.inserted_id:
            project_data["id"] = project_data.pop("_id")
            return {"message": "Проект успешно создан", "project": project_data}
        else:
            return {"error": "Не удалось создать проект"}

    except DuplicateKeyError:
        return {"error": "Проект с таким именем или кодом уже существует"}
    except Exception as e:
        return {"error": f"Ошибка при создании проекта: {str(e)}"}


def create_task(task_data: Dict[str, Any]) -> Dict[str, Any]:
    """Создает новую задачу в MongoDB"""
    try:
        project = projects_collection.find_one({"_id": task_data["project_id"]})
        if not project:
            return {"error": "Проект не найден"}

        task_id = str(uuid.uuid4())
        task_data["_id"] = task_id

        task_count = tasks_collection.count_documents({"project_id": task_data["project_id"]})
        task_data["code"] = f"{project['code']}-{task_count + 1}"

        result = tasks_collection.insert_one(task_data)

        if result.inserted_id:
            task_data["id"] = task_data.pop("_id")
            return {"message": "Задача успешно создана", "task": task_data}
        else:
            return {"error": "Не удалось создать задачу"}

    except Exception as e:
        return {"error": f"Ошибка при создании задачи: {str(e)}"}
