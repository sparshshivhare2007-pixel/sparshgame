# commands/chat.py
# AI Chat System – FINAL VERSION

import random
import httpx
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import ContextTypes
from telegram.constants import (
    ParseMode,
    ChatAction,
    ChatType
)

# -------------------- IMPORTS --------------------
from helpers.config import (
    BOT_NAME,
    OWNER_LINK,
    MISTRAL_API_KEY,
    GROQ_API_KEY,
    CODESTRAL_API_KEY
)

from helpers.utils import stylize_text
from database.mongo import chatbot_collection


# -------------------- BASIC CONFIG --------------------

BAKA_NAME = BOT_NAME or "Baka"

MAX_HISTORY = 8
DEFAULT_MODEL = "mistral"

EMOJI_POOL = [
    "✨", "💖", "🌸", "😊", "🥰",
    "💕", "🎀", "🌺", "💫", "🦋"
]

FALLBACK_RESPONSES = [
    "Hmm… achha 😊",
    "Samjha ✨",
    "Okk 💖",
    "Interesting 🌸",
    "Aur batao 🦋"
]


# -------------------- AI MODELS --------------------

MODELS = {
    "groq": {
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "model": "llama3-70b-8192",
        "key": GROQ_API_KEY
    },
    "mistral": {
        "url": "https://api.mistral.ai/v1/chat/completions",
        "model": "mistral-large-latest",
        "key": MISTRAL_API_KEY
    },
    "codestral": {
        "url": "https://codestral.mistral.ai/v1/chat/completions",
        "model": "codestral-latest",
        "key": CODESTRAL_API_KEY
    }
}


# -------------------- API CALL --------------------

async def call_model_api(provider, messages, max_tokens):
    conf = MODELS.get(provider)
    if not conf or not conf["key"]:
        return None

    headers = {
        "Authorization": f"Bearer {conf['key']}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": conf["model"],
        "messages": messages,
        "temperature": 0.8,
        "max_tokens": max_tokens
    }

    try:
        async with httpx.AsyncClient(timeout=25) as client:
            res = await client.post(conf["url"], headers=headers, json=payload)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[AI ERROR] {provider}: {e}")

    return None


# -------------------- AI CORE --------------------

async def get_ai_response(chat_id: int, text: str):
    code_keywords = [
        "code", "python", "html", "css", "js",
        "error", "debug", "class", "import", "function"
    ]

    is_code = any(k in text.lower() for k in code_keywords)

    if is_code:
        model = "codestral"
        max_tokens = 4000
        system_prompt = (
            "You are a professional coding assistant. "
            "Give clean, working code with short explanation."
        )
    else:
        model = DEFAULT_MODEL
        max_tokens = 200
        emoji = random.choice(EMOJI_POOL)
        system_prompt = (
            f"You are {BAKA_NAME}, a sweet Indian girlfriend. "
            "Reply in natural Hinglish. "
            "Use only one emoji like "
            f"{emoji}. Never say you are an AI."
        )

    doc = chatbot_collection.find_one({"chat_id": chat_id}) or {}
    history = doc.get("history", [])

    messages = [{"role": "system", "content": system_prompt}]
    messages += history[-MAX_HISTORY:]
    messages.append({"role": "user", "content": text})

    reply = await call_model_api(model, messages, max_tokens)

    if not reply:
        reply = await call_model_api("mistral", messages, max_tokens)

    if not reply:
        reply = random.choice(FALLBACK_RESPONSES)

    reply = reply.replace("*", "").strip()

    new_history = history + [
        {"role": "user", "content": text},
        {"role": "assistant", "content": reply}
    ]

    chatbot_collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"history": new_history[-(MAX_HISTORY * 2):]}},
        upsert=True
    )

    return reply, is_code


# -------------------- MESSAGE HANDLER --------------------

async def ai_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text or msg.text.startswith("/"):
        return

    chat = update.effective_chat

    if chat.type != ChatType.PRIVATE:
        doc = chatbot_collection.find_one({"chat_id": chat.id}) or {}
        if not doc.get("enabled", True):
            return

    await context.bot.send_chat_action(chat.id, ChatAction.TYPING)

    reply, is_code = await get_ai_response(chat.id, msg.text)

    if is_code:
        await msg.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
    else:
        await msg.reply_text(stylize_text(reply))


# -------------------- /chatbot MENU --------------------

async def chatbot_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🦙 Groq", callback_data="ai_groq"),
            InlineKeyboardButton("🌟 Mistral", callback_data="ai_mistral")
        ],
        [InlineKeyboardButton("🖥 Codestral", callback_data="ai_codestral")],
        [InlineKeyboardButton("🗑 Clear Memory", callback_data="ai_reset")]
    ])

    await update.message.reply_text(
        "🤖 <b>Baka AI Settings</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=kb
    )


async def chatbot_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    data = q.data
    chat_id = q.message.chat.id

    if data == "ai_reset":
        chatbot_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"history": []}},
            upsert=True
        )
        return await q.answer("Memory cleared 🧠", show_alert=True)

    model_map = {
        "ai_groq": "groq",
        "ai_mistral": "mistral",
        "ai_codestral": "codestral"
    }

    if data in model_map:
        chatbot_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"model": model_map[data]}},
            upsert=True
        )
        await q.answer("Model switched ✅", show_alert=True)


# -------------------- /ask COMMAND --------------------

async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text(
            "Usage: /ask <question>"
        )

    query = " ".join(context.args)
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)

    reply, is_code = await get_ai_response(update.effective_chat.id, query)

    if is_code:
        await update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text(stylize_text(reply))


# -------------------- MAIN.PY COMPAT --------------------
# main.py expects `chat_handler`
chat_handler = ai_message_handler
