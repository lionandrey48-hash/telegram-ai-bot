import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# --- ВСТАВЬ СЮДА ТОКЕН ---
TOKEN = "8490053226:AAGd5t4HAHYcdsCwmjqBQknYxqOEbDf-1sA"

dp = Dispatcher()

# 1. Главное меню (Кнопки внизу)
main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🎲 Бросить кубик"), KeyboardButton(text="📸 Хочу фото")],
    [KeyboardButton(text="🔗 Полезные ссылки")]
], resize_keyboard=True)

# 2. Инлайн-меню (Кнопки под сообщением)
links_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📺 YouTube", url="https://youtube.com")],
    [InlineKeyboardButton(text="🔎 Google", url="https://google.com")]
])

# Команда /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я обновился. Зацени меню 👇", reply_markup=main_kb)

# Бросок кубика
@dp.message(F.text == "🎲 Бросить кубик")
async def dice(message: Message):
    await message.answer_dice(emoji="🎰")

# Отправка ссылок (Инлайн)
@dp.message(F.text == "🔗 Полезные ссылки")
async def links(message: Message):
    await message.answer("Вот тебе пару кнопок-ссылок:", reply_markup=links_kb)

# Реакция на фото (Эхо)
# Если нажали "Хочу фото"
@dp.message(F.text == "📸 Хочу фото")
async def send_photo(message: Message):
    # Ссылка на картинку (можешь заменить на свою)
    photo_url = "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg"
    await message.answer_photo(photo=photo_url, caption="Держи красивое фото! 🌳")
@dp.message(F.photo)
async def photo_handler(message: Message):
    await message.answer("Ого, крутая фотка! 👍")

# Запуск
async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
