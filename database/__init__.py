from .users import users_db, user_db, users, get_user
from .groups import groups_db, is_group_open, set_group_status

# Tracking helpers used in main.py
def add_group_id(chat_id):
    groups_db.update_one(
        {"group_id": chat_id},
        {"$set": {"group_id": chat_id, "open": True}},
        upsert=True
    )

def add_message_count(user_id):
    users_db.update_one(
        {"user_id": user_id},
        {"$inc": {"messages_count": 1, "xp": 10}},
        upsert=True
    )
