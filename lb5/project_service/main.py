from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pymongo import MongoClient
from bson import ObjectId
from typing import List
from models import Project
from storage import projects_collection
from config import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def check_user_in_project(project: dict, user_id: int):
    if user_id not in project.get("members", []):
        raise HTTPException(status_code=403, detail="User is not a member of this project")

@app.post("/projects", response_model=Project)
def create_project(project: Project, current_user: dict = Depends(get_current_user)):
    project_dict = project.dict(exclude={"id"})
    if current_user["id"] not in project_dict.get("members", []):
        project_dict["members"] = project_dict.get("members", []) + [current_user["id"]]
    result = projects_collection.insert_one(project_dict)
    project.id = str(result.inserted_id)
    return project

@app.get("/projects", response_model=List[Project])
def get_projects(current_user: dict = Depends(get_current_user)):
    projects = []
    for project in projects_collection.find({"members": current_user["id"]}):
        project["id"] = str(project["_id"])
        del project["_id"]
        projects.append(Project(**project))
    return projects

@app.get("/projects/{project_id}", response_model=Project)
def get_project(project_id: str, current_user: dict = Depends(get_current_user)):
    project = projects_collection.find_one({"_id": ObjectId(project_id)})
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    check_user_in_project(project, current_user["id"])
    project["id"] = str(project["_id"])
    del project["_id"]
    return Project(**project)

@app.put("/projects/{project_id}", response_model=Project)
def update_project(project_id: str, updated_project: Project, current_user: dict = Depends(get_current_user)):
    project = projects_collection.find_one({"_id": ObjectId(project_id)})
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    check_user_in_project(project, current_user["id"])
    result = projects_collection.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": updated_project.dict(exclude={"id"})}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    updated_project.id = project_id
    return updated_project

@app.delete("/projects/{project_id}", response_model=Project)
def delete_project(project_id: str, current_user: dict = Depends(get_current_user)):
    project = projects_collection.find_one({"_id": ObjectId(project_id)})
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    check_user_in_project(project, current_user["id"])
    projects_collection.delete_one({"_id": ObjectId(project_id)})
    project["id"] = str(project["_id"])
    del project["_id"]
    return Project(**project)

@app.get("/projects/search/by-name", response_model=List[Project])
def search_projects_by_name(name: str, current_user: dict = Depends(get_current_user)):
    projects = []
    query = {"name": {"$regex": name, "$options": "i"}, "members": current_user["id"]}
    for project in projects_collection.find(query):
        project["id"] = str(project["_id"])
        del project["_id"]
        projects.append(Project(**project))
    if not projects:
        raise HTTPException(status_code=404, detail="No projects found with this name")
    return projects
