import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["economy_bot"]

# ---------------- COLLECTIONS ----------------
users = db["users"]
groups_db = db["groups"]

# ---------------- ALIASES (Sabhi files ke liye) ----------------
user_db = users   # main.py ke liye
users_db = users  # give.py ke liye
# groups_db collection ko bhi export karein taaki main.py broadcast chale
groups = groups_db 

# ---------------- USER FUNCTIONS ----------------
def get_user(user_id: int):
    user = users.find_one({"user_id": user_id})
    if not user:
        user = {"user_id": user_id, "balance": 0, "kills": 0, "killed": False, "protected": False, "messages": 0}
        users.insert_one(user)
    return user

def is_protected(user_id: int) -> bool:
    user = users.find_one({"user_id": user_id})
    return user.get("protected", False) if user else False

def add_message_count(user_id: int):
    users.update_one({"user_id": user_id}, {"$inc": {"messages": 1}}, upsert=True)

# ---------------- GROUP FUNCTIONS ----------------
def set_group_open(group_id: int, status: bool):
    groups_db.update_one({"group_id": group_id}, {"$set": {"open": status}}, upsert=True)

# Alias for open_economy.py
set_group_status = set_group_open 

def is_group_open(group_id: int) -> bool:
    group = groups_db.find_one({"group_id": group_id})
    return group.get("open", True) if group else True

def add_group_id(group_id: int):
    groups_db.update_one({"group_id": group_id}, {"$set": {"group_id": group_id, "open": True}}, upsert=True)
