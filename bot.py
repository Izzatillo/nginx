import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Токен из переменной окружения (безопаснее, чем в коде)
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Загружаем данные
with open("places.json", "r", encoding="utf-8") as file:
    PLACES = json.load(file)["places"]

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Еда", callback_data="food")],
        [InlineKeyboardButton("Семейный отдых", callback_data="family")],
        [InlineKeyboardButton("Вечер", callback_data="evening")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери категорию:", reply_markup=reply_markup)

# Обработка кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    category = query.data
    await query.answer()

    places = [p for p in PLACES if p["category"] == category]
    if places:
        for place in places:
            message = f"{place['name']}\n{place['description']}\n{place['location']}"
            await query.message.reply_photo(photo=place["image"], caption=message)
    else:
        await query.message.reply_text("Пока ничего нет в этой категории.")

# Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()