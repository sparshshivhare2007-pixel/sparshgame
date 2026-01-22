from datetime import datetime
from database.users import users_db

def is_protected(user_id):
    """Checks if a user has active protection (shield)."""
    user = users_db.find_one({"user_id": user_id})
    if not user or not user.get("protection_until"):
        return False, None
    
    until = user["protection_until"]
    # MongoDB stores datetime objects
    if datetime.utcnow() < until:
        return True, until - datetime.utcnow()
    return False, None

def format_delta(td):
    """Formats timedelta into '1d 5h 30m' style."""
    if not td: return "0m"
    secs = int(td.total_seconds())
    days, rem = divmod(secs, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)
    
    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    return " ".join(parts) if parts else "0m"

def tag(user):
    """Creates a clickable HTML tag for users."""
    name = user.first_name.replace("<", "").replace(">", "")
    return f"<a href='tg://user?id={user.id}'>{name}</a>"
