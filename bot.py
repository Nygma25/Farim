"""
Telegram Bot (aiogram) for IdeaFarm
Handles /start, referrals, notifications and launching Mini App
"""

import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.enums import ParseMode

from app.core.config import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user = message.from_user
    args = message.text.split(maxsplit=1)
    ref_code = args[1] if len(args) > 1 else None

    # TODO: Сохранить пользователя в БД + обработать рефералку

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Открыть IdeaFarm",
                    web_app=WebAppInfo(url=settings.WEBAPP_URL)
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Мои поинты и задания",
                    callback_data="show_stats"
                )
            ]
        ]
    )

    text = (
        f"Привет, {user.first_name}! 👋\n\n"
        "Добро пожаловать в <b>IdeaFarm</b> — место, где идеи превращаются в деньги.\n\n"
        "🌱 Фарми поинты каждый день\n"
        "💡 Генерируй монетизируемые идеи с Grok AI\n"
        "✅ Получай план запуска и заработка\n"
        "👥 Приглашай друзей и зарабатывай вместе\n\n"
        "Нажми кнопку ниже, чтобы начать фармить идеи!"
    )

    await message.answer(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


@dp.callback_query(lambda c: c.data == "show_stats")
async def show_stats(callback: types.CallbackQuery):
    # TODO: Получить реальные данные из БД
    await callback.message.answer(
        "📊 Твоя статистика:\n\n"
        "💰 IdeaPoints: 1 250\n"
        "🔥 Streak: 7 дней\n"
        "👥 Приглашено: 3 друга\n\n"
        "Открой Mini App, чтобы увидеть все задания!"
    )
    await callback.answer()


# TODO: Добавить хендлеры для уведомлений, рефералов и т.д.

async def send_notification(telegram_id: int, text: str):
    """Отправка уведомления пользователю"""
    try:
        await bot.send_message(telegram_id, text, parse_mode=ParseMode.HTML)
    except Exception as e:
        print(f"Failed to send notification to {telegram_id}: {e}")