from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from aiogram import Bot
import os
from pathlib import Path
from dotenv import load_dotenv
import asyncio
import json

# --- Настройка окружения ---
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / "keys.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

app = FastAPI()

DATA_FILE = BASE_DIR / "data.json"

@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    info = request.query_params.get("state")
    state = info.split("_")[0]
    id = info.split("_")[1]

    if code:
        # Сохраняем код в Python
        data = {id : {"code" : code}}

        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, DATA_FILE, ensure_ascii=False, indent=4)

        await bot.send_message(chat_id=int(state), text=f"Авторизация прошла успешно!")

    # Отдаем HTML пользователю
    with open(BASE_DIR / "callback.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
