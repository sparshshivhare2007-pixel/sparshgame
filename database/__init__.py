# database/__init__.py
from .users import get_user
from .groups import is_group_open, set_group_status
from .mongo import users, groups, chatbot_collection

# helper wrappers (agar main.py expect karta ho)
def add_group_id(chat_id: int):
    groups.update_one(
        {"group_id": chat_id},
        {"$set": {"group_id": chat_id}},
        upsert=True
    )

def add_message_count(user_id: int):
    users.update_one(
        {"user_id": user_id},
        {"$inc": {"messages": 1}},
        upsert=True
    )
