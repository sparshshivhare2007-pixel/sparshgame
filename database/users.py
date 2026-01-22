# database/users.py
from database.mongo import users
from datetime import datetime

def get_user(user_id: int):
    user = users.find_one({"user_id": user_id})
    if not user:
        user = {
            "user_id": user_id,
            "balance": 0,
            "bank": 0,
            "kills": 0,
            "messages": 0,
            "claimed": False,
            "protected": False,
            "created_at": datetime.utcnow()
        }
        users.insert_one(user)
    return user
