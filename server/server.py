from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from aiogram import Bot
import os
from pathlib import Path
from dotenv import load_dotenv
import asyncio

# --- Настройка окружения ---
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / "keys.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

app = FastAPI()

# Простое хранилище для code
codes_storage = {}

@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")  # здесь chat_id или любое значение

    if code:
        # Сохраняем код в Python
        codes_storage[state] = code
        print(f"Получен code={code} для state={state}")

        # Можно сразу отправить сообщение в Telegram (опционально)
        await bot.send_message(chat_id=int(state), text=f"Ваш EXBO code: {code}")

    # Отдаем HTML пользователю
    with open(BASE_DIR / "callback.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
