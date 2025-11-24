from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
import asyncio

API_TOKEN = "8457431448:AAGwVBaaxo9oS9U70dPygUwzwuiWOP0eUAo"
bot = Bot(API_TOKEN)
dp = Dispatcher()
app = FastAPI()

@app.post("/oauth")
async def oauth(request: Request):
    data = await request.json()
    code = data["code"]
    chat_id = data["state"]

    # можно обработать code прямо тут
    print("Получен code:", code)

    # уведомить пользователя (если нужно)
    await bot.send_message(chat_id, f"Код получен ботом!\ncode: {code}")

    return {"status": "ok"}

# запуск бота
@app.on_event("startup")
async def startup():
    asyncio.create_task(dp.start_polling(bot))
