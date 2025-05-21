import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from storage import projects_collection
from models import Project

MONGO_URL = "mongodb://mongo:27017/"

def wait_for_mongo():
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    while True:
        try:
            client.admin.command("ping")
            print("MongoDB доступен!")
            break
        except ConnectionFailure:
            print("Ожидание MongoDB...")
            time.sleep(2)
        finally:
            client.close()

def init_db():
    wait_for_mongo()

    if projects_collection.count_documents({}) == 0:
        test_projects = [
            Project(name="Project Alpha", description="First test project", members=[1, 2]),
            Project(name="Project Beta", description="Second test project", members=[1, 2, 3]),
        ]
        for project in test_projects:
            projects_collection.insert_one(project.dict())
        print("Test projects inserted successfully.")
    
    projects_collection.create_index("name")
    projects_collection.create_index("members")
    print("Indexes created on 'name' and 'members'.")

if __name__ == "__main__":
    init_db()
