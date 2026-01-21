# helpers/__init__.py

# 1. Database imports
from database.users import (
    get_user,
    users,
    user_db,
    users_db,
    is_protected,
    add_message_count,
    add_group_id,
    is_group_open,
    set_group_open,
    set_group_status
)

# 2. Utils imports
from .utils import format_delta, random_percentage, stylize_text

# 3. Import Config inside functions or handle properly to avoid circular import
import helpers.utils as utils

# AI Helpers
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
