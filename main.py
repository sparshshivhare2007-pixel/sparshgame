import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# -------------------- LOAD ENV --------------------
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID", "0"))

# -------------------- DATABASE --------------------
from database import (
    get_user,           # get user helper
    add_group_id,       # add group helper
    add_message_count,  # increment XP/messages
    users,              # users collection (MongoDB)
    groups,             # groups collection (MongoDB)
)

# -------------------- COMMANDS --------------------
from commands.start_command import start_command, button_handler
from commands.group_management import register_group_management
from commands.economy_guide import economy_guide
from commands.help_command import help_command
from commands.transfer_balance import transfer_balance
from commands.claim import claim
from commands.own import own
from commands.crush import crush
from commands.love import love
from commands.slap import slap
from commands.items import items
from commands.item import item
from commands.give import give
from commands.daily import daily
from commands.rob import rob
from commands.protect import protect
from commands.toprich import toprich
from commands.topkill import topkill
from commands.kill import kill
from commands.revive import revive
from commands.open_economy import open_economy
from commands.close_economy import close_economy
from commands.punch import punch
from commands.hug import hug
from commands.couple import couple
from commands.mine import mine
from commands.farm import farm
from commands.crime import crime
from commands.heal import heal
from commands.shop import shop
from commands.buy import buy
from commands.sell import sell
from commands.profile import profile
from commands.bank import bank
from commands.deposit import deposit
from commands.withdraw import withdraw

# ✅ AI CHAT
from commands.chat import ai_message_handler

# =====================================================
#                    BROADCAST
# =====================================================
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("⛔ Not authorized")

    if not context.args:
        return await update.message.reply_text("Usage: /broadcast <msg>")

    text = " ".join(context.args)
    sent, failed = 0, 0

    # Users loop
    for u in users.find():
        try:
            await context.bot.send_message(u["user_id"], text)
            sent += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1

    # Groups loop
    for g in groups.find():
        try:
            await context.bot.send_message(g["group_id"], text)
            sent += 1
            await asyncio.sleep(0.05)
        except:
            failed += 1

    await update.message.reply_text(
        f"📢 Broadcast Done\n✅ {sent} | ❌ {failed}"
    )

# -------------------- RESTART --------------------
async def test_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    await update.message.reply_text("🔄 Restarting…")
    os._exit(1)

# -------------------- TRACK USERS --------------------
async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    add_group_id(chat.id)

    if chat.type == "private":
        try:
            await context.bot.send_message(
                ADMIN_GROUP_ID,
                f"👤 {user.first_name} started bot",
            )
        except:
            pass

# -------------------- BALANCE --------------------
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    rank_data = list(users.find().sort("balance", -1))
    ids = [u["user_id"] for u in rank_data]
    rank = ids.index(user_id) + 1 if user_id in ids else "?"

    await update.message.reply_text(
        f"👤 {update.effective_user.first_name}\n"
        f"💰 Balance: {user['balance']}\n"
        f"🏆 Rank: #{rank}\n"
        f"⚔️ Kills: {user['kills']}"
    )

# -------------------- WORK --------------------
async def work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    users.update_one(
        {"user_id": user_id},
        {"$inc": {"balance": 200}}
    )
    await update.message.reply_text("💼 You earned 200 coins!")

# -------------------- ERROR --------------------
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print("ERROR:", context.error)

# -------------------- AI + XP --------------------
async def ai_group_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text:
        return

    add_message_count(msg.from_user.id)

    if msg.chat.type == "private":
        return await ai_message_handler(update, context)

    if context.bot.username.lower() in msg.text.lower():
        return await ai_message_handler(update, context)

    if msg.reply_to_message and msg.reply_to_message.from_user.id == context.bot.id:
        return await ai_message_handler(update, context)

# -------------------- MAIN --------------------
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_error_handler(error_handler)

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, track_users))
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("test", test_restart))
    app.add_handler(CommandHandler("broadcast", broadcast))

    economy_cmds = [
        ("balance", balance), ("work", work), ("economy", economy_guide),
        ("transfer", transfer_balance), ("claim", claim), ("own", own),
        ("crush", crush), ("love", love), ("slap", slap),
        ("items", items), ("item", item), ("give", give), ("daily", daily),
        ("rob", rob), ("protect", protect), ("toprich", toprich),
        ("topkill", topkill), ("kill", kill), ("revive", revive),
        ("open", open_economy), ("close", close_economy)
    ]
    for c, h in economy_cmds:
        app.add_handler(CommandHandler(c, h))

    fun_cmds = [("punch", punch), ("hug", hug), ("couple", couple)]
    for c, h in fun_cmds:
        app.add_handler(CommandHandler(c, h))

    hidden_cmds = [
        ("mine", mine), ("farm", farm), ("crime", crime),
        ("heal", heal), ("shop", shop), ("buy", buy),
        ("sell", sell), ("profile", profile),
        ("bank", bank), ("deposit", deposit),
        ("withdraw", withdraw)
    ]
    for c, h in hidden_cmds:
        app.add_handler(CommandHandler(c, h))

    register_group_management(app)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_group_filter))

    print("🚀 Bot Started Successfully")
    app.run_polling()

if __name__ == "__main__":
    main()
