from aiogram import Bot, Dispatcher, types, filters
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

from server import get_auth_code_by_user_id

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
    # Получаем user_id как строку и обрабатываем результат
    user_id = str(message.from_user.id)
    auth_code = await get_auth_code_by_user_id(user_id)
    
    if auth_code:
        await message.answer(f"Ваш код авторизации: {auth_code}")
    else:
        await message.answer("Код авторизации не найден. Пожалуйста, сначала авторизуйтесь через /auth")
# Запуск бота


@dp.message(filters.Command("clean"))
async def start_handler(message: types.Message):
    await message.answer(str(message.from_user.id))
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
