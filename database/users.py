# database/users.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI not found in environment variables")

client = MongoClient(MONGO_URI)

db = client["economy_bot"]

# ---------------- COLLECTIONS ----------------
users = db["users"]
groups_db = db["groups"]

# ---------------- USER FUNCTIONS ----------------
def get_user(user_id: int):
    user = users.find_one({"user_id": user_id})
    if not user:
        user = {
            "user_id": user_id,
            "balance": 0,
            "kills": 0,
            "killed": False,
            "protected": False,
            "messages": 0
        }
        users.insert_one(user)
    return user


def add_message_count(user_id: int):
    users.update_one(
        {"user_id": user_id},
        {"$inc": {"messages": 1}},
        upsert=True
    )


# ---------------- GROUP FUNCTIONS ----------------
def add_group_id(group_id: int):
    groups_db.update_one(
        {"group_id": group_id},
        {"$set": {"group_id": group_id, "open": True}},
        upsert=True
    )


def is_group_open(group_id: int) -> bool:
    group = groups_db.find_one({"group_id": group_id})
    if not group:
        add_group_id(group_id)
        return True
    return group.get("open", True)


def set_group_open(group_id: int, status: bool):
    groups_db.update_one(
        {"group_id": group_id},
        {"$set": {"open": status}},
        upsert=True
    )


# alias used in main.py
user_db = users
