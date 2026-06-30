import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# TOKEN береться з Railway / Render
TOKEN = os.environ.get("TOKEN")

OWNER_ID = 5904220441

# зберігаємо апеляції
appeals = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Напиши апеляцію:\n\n"
        "Нік:\nПричина бану:\nЧому вважаєш бан помилкою:"
    )

# отримання апеляції
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    text = update.message.text

    appeals[user_id] = text

    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"""📩 НОВА АПЕЛЯЦІЯ

ID: {user_id}

{text}

💬 Відповідь:
`/reply {user_id} твій текст`"""
    )

    await update.message.reply_text("Апеляцію отримано, очікуйте відповідь.")

# відповідь гравцю
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

# запуск
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reply", reply))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()