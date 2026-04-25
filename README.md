# 🚀 Space Shop — Telegram Mini App

Магазин космического мерча на базе Telegram Mini Apps.

## Стек технологий

- **Backend:** Python 3.10+, Aiogram 3.x, FastAPI, Uvicorn
- **Frontend:** HTML5, Pico.css, Telegram Web App SDK
- **Валидация:** Pydantic
- **Безопасность:** HMAC-SHA256 проверка initData

## Структура проекта

| Файл | Описание |
|------|----------|
| `bot.py` | Telegram-бот (Aiogram 3.x) — команда /start с WebApp-кнопкой |
| `main.py` | Веб-сервер (FastAPI) — отдает фронтенд и обрабатывает заказы |
| `index.html` | Фронтенд Mini App — карточка товара, Telegram SDK |
| `requirements.txt` | Зависимости проекта |

## Установка и запуск

```bash
# Установка зависимостей
pip install -r requirements.txt

# Установка переменных окружения
export BOT_TOKEN="ваш_токен_бота"
export WEBAPP_URL="https://ваш-домен.com"

# Запуск веб-сервера
python main.py

# Запуск бота (в отдельном терминале)
python bot.py
```

## Деплой (Uptime 24/7)

Для поддержания сервера на Replit в рабочем состоянии 24/7:

1. Зарегистрируйтесь на [UptimeRobot](https://uptimerobot.com/)
2. Создайте новый монитор типа **HTTP(s)**
3. Укажите URL вашего сервера на Replit
4. Установите интервал проверки — **5 минут**

Сервис будет «пинговать» ваш сервер каждые 5 минут, не давая ему «заснуть».
