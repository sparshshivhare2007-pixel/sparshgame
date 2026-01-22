# database/users.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("❌ MONGO_URI not found")

client = MongoClient(MONGO_URI)
db = client["economy_bot"]

# ---------------- COLLECTION ----------------
users = db["users"]


# ---------------- USER FUNCTIONS ----------------
def get_user(user_id: int):
    user = users.find_one({"user_id": user_id})

    if not user:
        user = {
            "user_id": user_id,
            "balance": 0,
            "bank": 0,
            "claimed": False,
            "messages": 0,
            "kills": 0,
            "protected": False
        }
        users.insert_one(user)

    return user
