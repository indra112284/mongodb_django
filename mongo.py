import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = quote_plus(os.getenv("MONGO_PASSWORD"))
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
MONGO_DATABASE = os.getenv("MONGO_DATABASE")
MONGO_AUTH_SOURCE = os.getenv("MONGO_AUTH_SOURCE")

MONGO_URL = (
    f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}"
    f"@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE}"
    f"?authSource={MONGO_AUTH_SOURCE}"
)

client = MongoClient(MONGO_URL)

db = client[MONGO_DATABASE]

students_collection = db["students"]

departments_collection = db["departments"]