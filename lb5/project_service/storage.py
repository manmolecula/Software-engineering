from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017/")
db = client["project_db"]
projects_collection = db["projects"]
