from aiogram import Bot, Dispatcher, types, filters
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import os
from pathlib import Path
import re
from server import get_code
from dotenv import load_dotenv

# Загружаем токен
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / "keys.env") 

API_TOKEN = os.getenv("BOT_TOKEN")
print(API_TOKEN)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Команда /auth
@dp.message(filters.Command("auth"))
async def start_handler(message: types.Message):
    url = f"https://exbo.net/oauth/authorize?client_id=788&redirect_uri=https://sc-x-db-bot.onrender.com/callback&response_type=code&state={message.chat.id}_{message.from_user.id}"
    auth_button = InlineKeyboardButton(
        text="Войти через EXBO",
        url=url
    )
    # inline_keyboard — список списков кнопок
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[auth_button]])

    await message.answer("Привет! Авторизуйтесь через EXBO:", reply_markup=keyboard)


@dp.message(filters.Command("start"))
async def start_handler(message: types.Message):
    ...

# Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
