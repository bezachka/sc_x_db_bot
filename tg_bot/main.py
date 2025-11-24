from aiogram import Bot, Dispatcher, types, filters
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import os
from pathlib import Path
import re
from dotenv import load_dotenv

# Загружаем токен
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / "keys.env") 

API_TOKEN = os.getenv("BOT_TOKEN")
print(API_TOKEN)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(filters.Command("start"))
async def start_handler(message: types.Message):
    url = f"https://exbo.net/oauth/authorize?client_id=788&redirect_uri=https://sc-x-db-bot.onrender.com/callback&response_type=code&state={message.chat.id}"
    auth_button = InlineKeyboardButton(
        text="Войти через EXBO",
        url=url
    )
    # inline_keyboard — список списков кнопок
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[auth_button]])

    await message.answer("Привет! Авторизуйтесь через EXBO:", reply_markup=keyboard)

@dp.message()
async def oauth_handler(message: types.Message):
    if message.text and message.text.startswith("exbo_oauth_code:"):
        code = message.text.split(":")[1]
        print("CODE =", code)
        await message.delete()
        await message.answer("Авторизация успешно завершена!")


# Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
