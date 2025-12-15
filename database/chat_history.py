from pymongo import MongoClient
import os
from datetime import datetime

# ❌ dotenv use mat karo (Heroku me kaam nahi karta)
# from dotenv import load_dotenv
# load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("❌ MONGO_URI environment variable not set")

client = MongoClient(MONGO_URI)
db = client["chatbot_db"]

# 🔥 Collection used by chat.py
chat_history = db["chat_history"]


def save_message(user_id: int, role: str, content: str):
    """
    Save a single chat message
    role -> 'user' | 'assistant'
    """
    chat_history.insert_one({
        "user_id": user_id,
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow()
    })


def get_last_messages(user_id: int, limit: int = 10):
    """
    Fetch last N messages for context
    """
    messages = chat_history.find(
        {"user_id": user_id}
    ).sort("timestamp", -1).limit(limit)

    history = []
    for msg in reversed(list(messages)):
        history.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    return history
