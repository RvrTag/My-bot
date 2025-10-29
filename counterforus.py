from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import re
import json
import os

# === НАСТРОЙКИ ===
TOKEN = "8421406905:AAH68tjstAwr_x9smttThxUMul4MsLGpSyo"  # <-- вставь токен, выданный BotFather
TARGET_ROOT = "отчисл"     # корень слова, по которому ищем
DATA_FILE = "group_counts.json"  # файл для хранения счётчиков


# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===
def load_counts():
    """Загружает счётчики из файла."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_counts(counts):
    """Сохраняет счётчики в файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(counts, f, ensure_ascii=False, indent=2)


# === ОСНОВНАЯ ФУНКЦИЯ ДЛЯ СЧЁТА СООБЩЕНИЙ ===
async def count_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = str(update.message.chat_id)
    text = update.message.text.lower()

    # Проверяем, есть ли слово с корнем "отчисл"
    if re.search(rf"\b{TARGET_ROOT}\w*\b", text):
        counts = load_counts()
        counts[chat_id] = counts.get(chat_id, 0) + 1
        save_counts(counts)

        count = counts[chat_id]
        await update.message.reply_text(f"+1, счётчик отчислений: {count}")


# === КОМАНДА /count ДЛЯ ПРОСМОТРА ТЕКУЩЕГО ЗНАЧЕНИЯ ===
async def show_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat_id)
    counts = load_counts()
    count = counts.get(chat_id, 0)
    await update.message.reply_text(f"Счётчик отчислений: {count}")


# === ЗАПУСК БОТА ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # обработка обычных сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count_messages))
    # команда /count
    app.add_handler(CommandHandler("count", show_count))

    print("Бот запущен и ждёт сообщений...")
    app.run_polling()


if __name__ == "__main__":
    main()
