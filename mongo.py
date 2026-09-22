from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

db = client["College_management"]

students_collection = db["students"]
departments_collection = db["departments"]