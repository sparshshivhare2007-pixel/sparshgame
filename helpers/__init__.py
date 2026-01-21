from database.users import (
    get_user,
    users,
    user_db,
    users_db,
    add_message_count,
    add_group_id,
    is_group_open,
    set_group_open
)
from .utils import format_delta, random_percentage

set_group_status = set_group_open

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
