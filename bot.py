from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8796227791:AAHfn877HrnEcCrtCH5W7MG1pdUQWiooTw8"
OWNER_ID = 5904220441

# зберігаємо останні апеляції (user_id -> info)
appeals = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Напиши апеляцію:\n\n"
        "Нік:\nПричина бану:\nЧому вважаєш бан помилкою:"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    text = update.message.text

    # зберігаємо апеляцію
    appeals[user_id] = text

    # відправляємо адміну
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"📩 НОВА АПЕЛЯЦІЯ\n\nID: {user_id}\n\n{text}\n\n"
             f"Відповідь: /reply {user_id} текст"
    )

    await update.message.reply_text("Апеляцію отримано, чекай відповіді.")

# команда відповіді гравцю
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != OWNER_ID:
        return

    try:
        user_id = int(context.args[0])
        text = " ".join(context.args[1:])

        await context.bot.send_message(
            chat_id=user_id,
            text=f"📢 ВІДПОВІДЬ ВІД САПОРТУ:\n\n{text}"
        )

        await update.message.reply_text("✅ Відправлено!")

    except:
        await update.message.reply_text("❌ Використання: /reply user_id текст")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reply", reply))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()