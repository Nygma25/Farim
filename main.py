"""
IdeaFarm - Telegram Mini App Backend
Main FastAPI application + aiogram bot integration
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.core.config import settings
from app.bot.bot import dp, bot
from app.api import router as api_router

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 IdeaFarm Backend starting...")
    # Здесь можно подключать БД, Redis и т.д.
    yield
    # Shutdown
    print("👋 IdeaFarm Backend shutting down...")


app = FastAPI(
    title="IdeaFarm API",
    description="Backend for IdeaFarm Telegram Mini App (Blum-style idea farming)",
    version="0.1.0",
    lifespan=lifespan
)

# CORS для Mini App (Telegram WebView)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене ограничить домен Mini App
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем API роуты
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "IdeaFarm API is running 🚀",
        "docs": "/docs",
        "mini_app": settings.WEBAPP_URL
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


# Пример: эндпоинт для получения данных пользователя (заглушка)
@app.get("/api/me")
async def get_me(request: Request):
    # TODO: Здесь будет валидация Telegram initData
    # и получение/создание пользователя в БД
    return {
        "telegram_id": 123456789,
        "username": "example_user",
        "points": 1250,
        "streak": 7,
        "is_premium": False
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)