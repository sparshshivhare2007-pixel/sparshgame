import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB Connection
MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client['myra_bot_db']

# Collections (Mapping all names used in your 41 commands)
users_db = db['users']
user_db = users_db 
users = users_db

def get_user(user_id):
    user = users_db.find_one({"user_id": user_id})
    if not user:
        user_data = {
            "user_id": user_id,
            "balance": 1000,        # Starting balance
            "bank": 0,
            "user_level": 1,
            "xp": 0,
            "kills": 0,
            "killed": False,
            "items": [],            # Inventory for /buy, /sell, /items
            "protection_until": None, # For /protect
            "messages_count": 0,
            "badge": "🟢 Rookie"
        }
        users_db.insert_one(user_data)
        return user_data
    return user
