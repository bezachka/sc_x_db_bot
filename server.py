from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from aiogram import Bot
import os
import asyncpg
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / "keys.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")  # Добавляем эту строку

bot = Bot(token=BOT_TOKEN)
app = FastAPI()

async def init_db():
    """Создаем таблицу при старте"""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS auth_codes (
                id SERIAL PRIMARY KEY,
                user_id TEXT UNIQUE NOT NULL,
                code TEXT NOT NULL,
                state TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await conn.close()
        print("✅ База данных готова")
    except Exception as e:
        print(f"❌ Ошибка базы: {e}")

@app.on_event("startup")
async def startup():
    await init_db()

async def save_to_db(user_id: str, code: str, state: str):
    """Сохраняем в PostgreSQL"""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute('''
            INSERT INTO auth_codes (user_id, code, state) 
            VALUES ($1, $2, $3)
        ''', user_id, code, state)
        await conn.close()
        return True
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return False

@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    info = request.query_params.get("state")
    
    if code and info:
        state = info.split("_")[0]
        user_id = info.split("_")[1]
        
        # Сохраняем в базу вместо JSON
        success = await save_to_db(user_id, code, state)
        
        if success:
            await bot.send_message(
                chat_id=int(state), 
                text="✅ Авторизация успешна! Данные в базе."
            )
        else:
            await bot.send_message(
                chat_id=int(state), 
                text="⚠️ Ошибка сохранения"
            )

    with open(BASE_DIR / "callback.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)