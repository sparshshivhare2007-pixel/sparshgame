# database/__init__.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Sync MongoDB client
client = MongoClient(MONGO_URI)
db = client["economy_bot"]

# Collections
users_db = db["users"]
groups_db = db["groups"]
couples_db = db["couples"]
# helpers/__init__.py

chatai = db["chatai"]
chat_lang_db = db["ChatLangDb"]
chatbot_status_db = db["chatbot_status_db"]
# -------------------- IMPORTS FROM DATABASE --------------------
from database.users import (
    get_user,
    users,
    user_db,
    add_group_id,
    is_group_open,
    set_group_open   # ✅ correct name
)

runtime_users = set()
runtime_groups = set()
# backward compatibility
set_group_status = set_group_open

# -------- USERS --------
def get_user(user_id: int):
    user = users_db.find_one({"user_id": user_id})
    if not user:
        new_user = {
            "user_id": user_id,
            "balance": 0,
            "bank": 0,
            "kills": 0,
            "killed": False,
            "daily_cooldown": 0
        }
        users_db.insert_one(new_user)
        return new_user
    return user


# -------- GROUPS --------
def add_group_id(group_id: int):
    groups_db.update_one(
        {"group_id": group_id},
        {"$set": {"group_id": group_id}},
        upsert=True
    )

def is_group_open(group_id: int):
    group = groups_db.find_one({"group_id": group_id})
    return group.get("status") == "open" if group else False

def set_group_status(group_id: int, status: str):
    groups_db.update_one(
        {"group_id": group_id},
        {"$set": {"status": status}},
        upsert=True
    )
# -------------------- OPENAI GPT HELPER --------------------
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

async def ask_gpt(prompt: str, model: str = "gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"
