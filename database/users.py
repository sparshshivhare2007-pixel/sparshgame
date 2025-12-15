# database/users.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI not found in environment variables")

client = MongoClient(MONGO_URI)

# ✅ THIS WAS MISSING
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


def add_group_id(group_id: int):
    groups_db.update_one(
        {"group_id": group_id},
        {"$set": {"group_id": group_id}},
        upsert=True
    )


def add_message_count(user_id: int):
    users.update_one(
        {"user_id": user_id},
        {"$inc": {"messages": 1}},
        upsert=True
    )


# alias used in main.py
user_db = users
