# helpers/config.py

import os

# ---------------- BOT INFO ----------------
BOT_NAME = os.getenv("BOT_NAME", "Baka")
OWNER_LINK = os.getenv("OWNER_LINK", "https://t.me/yourusername")

# ---------------- API KEYS ----------------
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
CODESTRAL_API_KEY = os.getenv("CODESTRAL_API_KEY", "")
