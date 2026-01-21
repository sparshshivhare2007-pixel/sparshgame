# helpers/__init__.py

# -------------------- IMPORTS FROM DATABASE --------------------
# Kyunki aapne saara logic database/users.py mein rakha hai, 
# isliye hum saare functions wahin se mangwayenge.
from database.users import (
    get_user,
    users,
    user_db,
    users_db,        # Added this for give.py compatibility
    add_group_id,
    is_group_open,
    set_group_open
)

# 🔁 backward compatibility
set_group_status = set_group_open


# -------------------- OPENAI GPT HELPER --------------------
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

async def ask_gpt(prompt: str, model: str = "gpt-3.5-turbo"):
    try:
        # Note: openai version 1.0.0+ use kar rahe hain toh syntax thoda alag ho sakta hai
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"
