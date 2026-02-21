import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# --- ВСТАВЬ СЮДА ТОКЕН ---
TOKEN = "8490053226:AAGd5t4HAHYcdsCwmjqBQknYxqOEbDf-1sA"

dp = Dispatcher()
bot = Bot(token=TOKEN)

# --- БЛОК БОТА (Кнопки и логика) ---

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🎲 Бросить кубик"), KeyboardButton(text="📸 Хочу фото")],
    [KeyboardButton(text="🔗 Полезные ссылки")]
], resize_keyboard=True)

links_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📺 YouTube", url="https://youtube.com")],
    [InlineKeyboardButton(text="🔎 Google", url="https://google.com")]
])

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Я онлайн 24/7! 😎", reply_markup=main_kb)

@dp.message(F.text == "🎲 Бросить кубик")
async def dice(message: Message):
    await message.answer_dice(emoji="🎰")

@dp.message(F.text == "🔗 Полезные ссылки")
async def links(message: Message):
    await message.answer("Лови ссылки:", reply_markup=links_kb)

@dp.message(F.text == "📸 Хочу фото")
async def send_photo(message: Message):
    await message.answer_photo(photo="https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg", caption="Держи фото!")

# --- БЛОК "ОБМАНКИ" (Веб-сервер для Render) ---

async def handle(request):
    return web.Response(text="Бот работает!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    # Render выдает порт через переменную окружения PORT. Если её нет - берем 8080
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    # Запускаем и веб-сервер (чтобы не убили), и бота
    await asyncio.gather(
        start_web_server(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
