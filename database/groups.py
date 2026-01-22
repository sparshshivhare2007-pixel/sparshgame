# database/groups.py
from .users import db

groups = db["groups"]


def add_group_id(group_id: int):
    groups.update_one(
        {"group_id": group_id},
        {"$set": {"group_id": group_id, "open": True}},
        upsert=True
    )


def is_group_open(group_id: int) -> bool:
    group = groups.find_one({"group_id": group_id})
    if not group:
        add_group_id(group_id)
        return True
    return group.get("open", True)


def set_group_open(group_id: int, status: bool):
    groups.update_one(
        {"group_id": group_id},
        {"$set": {"open": status}},
        upsert=True
    )


# backward compatibility
set_group_status = set_group_open
