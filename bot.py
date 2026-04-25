"""
bot.py — «Мозг» бота: обрабатывает команды и открывает Mini App.
Используется Aiogram 3.x для асинхронной работы с Telegram Bot API.
"""

import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

# Токен бота — хранится в переменной окружения для безопасности
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")

# URL Mini App — адрес, по которому Telegram откроет ваше приложение
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-url.com")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    """Обработчик команды /start — отправляет клавиатуру с кнопкой Mini App."""
    # Кнопка с WebAppInfo открывает Mini App прямо внутри Telegram
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="Открыть приложение",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ]
        ],
        resize_keyboard=True,
    )
    await message.answer(
        "Добро пожаловать в Space Shop! 🚀\nНажмите кнопку ниже, чтобы открыть магазин.",
        reply_markup=keyboard,
    )


async def main() -> None:
    """Асинхронный запуск бота."""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
