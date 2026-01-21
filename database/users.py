import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Database Connection
MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client['myra_bot_db']

# Collections
users_db = db['users']
users = users_db  # Dono names support karne ke liye alias

def get_user(user_id):
    user = users_db.find_one({"user_id": user_id})
    if not user:
        user_data = {
            "user_id": user_id,
            "balance": 1000,       # Joining bonus
            "bank": 0,
            "user_level": 1,
            "xp": 0,
            "kills": 0,
            "killed": False,
            "items": [],
            "protection_until": None,
            "messages_count": 0,
            "badge": "🟢 Rookie"
        }
        users_db.insert_one(user_data)
        return user_data
    return user
