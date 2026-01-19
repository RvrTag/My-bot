from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import re
import json
import os

# === НАСТРОЙКИ ===
TOKEN = "8421406905:AAH68tjstAwr_x9smttThxUMul4MsLGpSyo"  
TARGET_ROOT = "отчисл"     
DATA_FILE = "group_counts.json"


# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===
def load_counts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_counts(counts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(counts, f, ensure_ascii=False, indent=2)


# === ОСНОВНАЯ ФУНКЦИЯ ДЛЯ СЧЁТА СООБЩЕНИЙ ===
async def count_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = str(update.message.chat_id)
    text = update.message.text.lower()

    # === SET COUNT ===
    # команда: set count N
    match = re.match(r"set\s+count\s+(\d+)", text)
    if match:
        new_value = int(match.group(1))
        counts = load_counts()
        counts[chat_id] = new_value
        save_counts(counts)

        await update.message.reply_text(f"Счётчик установлен на {new_value}")
        return  # чтобы не срабатывало остальное

    # === ОБЫЧНЫЙ СЧЁТ ===
    if re.search(rf"\b{TARGET_ROOT}\w*\b", text):
        counts = load_counts()
        counts[chat_id] = counts.get(chat_id, 0) + 1
        save_counts(counts)

        count = counts[chat_id]
        await update.message.reply_text(f"+1, счётчик отчислений: {count}")


# === КОМАНДА /count ===
async def show_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat_id)
    counts = load_counts()
    count = counts.get(chat_id, 0)
    await update.message.reply_text(f"Счётчик отчислений: {count}")


# === ЗАПУСК БОТА ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count_messages))
    app.add_handler(CommandHandler("count", show_count))

    print("Бот запущен и ждёт сообщений...")
    app.run_polling()


if __name__ == "__main__":
    main()