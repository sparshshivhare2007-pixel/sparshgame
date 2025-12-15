# database/groups.py
from database.mongo import groups

def add_group_id(group_id: int):
    if not groups.find_one({"group_id": group_id}):
        groups.insert_one({
            "group_id": group_id,
            "economy_open": True
        })

def is_group_open(group_id: int) -> bool:
    group = groups.find_one({"group_id": group_id})
    return group.get("economy_open", True) if group else True

def set_group_status(group_id: int, status: bool):
    groups.update_one(
        {"group_id": group_id},
        {"$set": {"economy_open": status}},
        upsert=True
    )
