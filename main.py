import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

TOKEN = os.getenv("TOKEN")

dp = Dispatcher()
bot = Bot(token=TOKEN)

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

def search_knowledge(question):
    with open('knowledge_base.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    blocks = content.strip().split('\n\n')
    question_lower = question.lower()
    for block in blocks:
        if any(word in block.lower() for word in question_lower.split()):
            if 'Ответ:' in block:
                return block.split('Ответ:')[1].strip()
    return "Извините, не нашёл ответ. Попробуйте переформулировать."

@dp.message()
async def handle_question(message: Message):
    answer = search_knowledge(message.text)
    await message.answer(answer)

async def handle(request):
    return web.Response(text="Бот работает!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '[jg:ip_address_77]', port)
    await site.start()

async def main():
    await asyncio.gather(start_web_server(), dp.start_polling(bot))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
