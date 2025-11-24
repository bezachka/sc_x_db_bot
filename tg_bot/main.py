from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
import asyncio
import os

API_TOKEN = os.getenv("BOT_TOKEN")  # токен бота из переменных окружения
bot = Bot(API_TOKEN)
dp = Dispatcher()
app = FastAPI()

# Endpoint для получения code
@app.post("/oauth")
async def oauth(request: Request):
    data = await request.json()
    code = data.get("code")
    chat_id = data.get("state")

    if code and chat_id:
        await bot.send_message(chat_id, f"Ваш EXBO code: {code}")
        print(f"Получен code: {code} для chat_id: {chat_id}")
        return {"status": "ok"}
    return {"status": "error", "message": "Missing code or state"}

# Запуск бота
@app.on_event("startup")
async def startup():
    asyncio.create_task(dp.start_polling(bot))