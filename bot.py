import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# TOKEN з Railway / Render (захист від \n і пробілів)
TOKEN = os.getenv("TOKEN", "").strip()

# твій Telegram ID
OWNER_ID = 5904220441

# просте збереження апеляцій
appeals = {}

# --------------------
# START
# --------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! 👋\n\n"
        "Надішли апеляцію у форматі:\n\n"
        "Нік:\nПричина бану:\nЧому вважаєш бан помилкою:"
    )

# --------------------
# ОТРИМАННЯ АПЕЛЯЦІЇ
# --------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.effective_chat.id
    text = update.message.text

    # зберігаємо
    appeals[user_id] = text

    # відправляємо адміну
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=(
            "📩 НОВА АПЕЛЯЦІЯ\n\n"
            f"ID: {user_id}\n\n"
            f"{text}\n\n"
            f"💬 Відповідь:\n/reply {user_id} <текст>"
        )
    )

    await update.message.reply_text("✅ Апеляцію отримано, очікуйте відповідь.")

# --------------------
# ВІДПОВІДЬ АДМІНА
# --------------------
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != OWNER_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text("❌ Використання: /reply user_id текст")
        return

    user_id = int(context.args[0])
    text = " ".join(context.args[1:])

    await context.bot.send_message(
        chat_id=user_id,
        text=f"📢 ВІДПОВІДЬ ВІД САПОРТУ:\n\n{text}"
    )

    await update.message.reply_text("✅ Відправлено!")

# --------------------
# СТАРТ БОТА
# --------------------
if not TOKEN:
    raise ValueError("TOKEN не знайдено! Додай його в Environment Variables")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reply", reply))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
