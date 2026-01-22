# database/users.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI missing")

client = MongoClient(MONGO_URI)
db = client["economy_bot"]

# collections
users = db["users"]
users_db = users      # 👈 tumhare import ke liye
user_db = users       # 👈 backward compatibility


def get_user(user_id: int):
    user = users.find_one({"user_id": user_id})

    if not user:
        user = {
            "user_id": user_id,
            "balance": 0,
            "bank": 0,
            "claimed": False,
            "messages_count": 0,
            "xp": 0,
            "kills": 0,
            "protected": False
        }
        users.insert_one(user)

    return user
