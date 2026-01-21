# helpers/__init__.py

# -------------------- IMPORTS FROM DATABASE --------------------
from database.users import (
    get_user,
    users,
    user_db
)

from database.groups import (
    add_group_id,
    is_group_open,
    set_group_open
)

# 🔁 backward compatibility (purane code ke liye)
set_group_status = set_group_open


# -------------------- OPENAI GPT HELPER --------------------
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

async def ask_gpt(prompt: str, model: str = "gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"
