import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["economy_bot"]

# Collections
users = db["users"]
groups_db = db["groups"]

# Aliases for compatibility
users_db = users  # Fixes give.py error
user_db = users   # Fixes main.py error

def get_user(user_id: int):
    user = users.find_one({"user_id": user_id})
    if not user:
        user = {"user_id": user_id, "balance": 0, "kills": 0, "killed": False, "protected": False, "messages": 0}
        users.insert_one(user)
    return user

def set_group_open(group_id: int, status: bool):
    groups_db.update_one({"group_id": group_id}, {"$set": {"open": status}}, upsert=True)

def is_group_open(group_id: int) -> bool:
    group = groups_db.find_one({"group_id": group_id})
    return group.get("open", True) if group else True

def add_group_id(group_id: int):
    groups_db.update_one({"group_id": group_id}, {"$set": {"group_id": group_id, "open": True}}, upsert=True)
