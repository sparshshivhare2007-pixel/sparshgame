from database.users import db

groups_db = db['groups']

def is_group_open(chat_id):
    group = groups_db.find_one({"chat_id": chat_id})
    if not group:
        return True  # Default: Economy Open
    return group.get("open", True)

def set_group_status(chat_id, status: bool):
    groups_db.update_one(
        {"chat_id": chat_id},
        {"$set": {"open": status}},
        upsert=True
    )
