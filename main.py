"""
main.py — «Мозг» сервера: принимает запросы от Mini App и обрабатывает заказы.
FastAPI — современный асинхронный веб-фреймворк Python.

Метафора: API — это «официант», который несет заказ клиента на «кухню» (бэкенд),
проверяет его и возвращает результат обратно.
"""

import hashlib
import hmac
import os
from urllib.parse import parse_qs

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Токен бота — нужен для проверки подписи initData (HMAC-SHA256)
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")

app = FastAPI(title="Space Shop API")

# --- CORS — разрешаем браузеру обращаться к нашему API ---
# Без этого браузер заблокирует fetch()-запросы с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Модель данных (Pydantic) ---
# Pydantic — «охранник» нашего API: проверяет, что данные пришли в правильном формате.
# Если клиент пришлет мусор вместо заказа, Pydantic вернет ошибку 422.
class Order(BaseModel):
    item_name: str
    amount: int


# --- Безопасность — «Замок нашего приложения» ---
# Никогда не доверяй фронтенду! Проверяем цифровую подпись initData,
# чтобы убедиться, что запрос действительно пришел из Telegram.
def validate_init_data(init_data: str, bot_token: str) -> bool:
    """Проверка подписи initData по алгоритму HMAC-SHA256."""
    try:
        parsed = parse_qs(init_data)
        # Извлекаем хеш, присланный Telegram
        received_hash = parsed.get("hash", [None])[0]
        if not received_hash:
            return False

        # Собираем строку для проверки: все параметры кроме hash, отсортированные по ключу
        data_check_pairs = []
        for key, values in parsed.items():
            if key == "hash":
                continue
            data_check_pairs.append(f"{key}={values[0]}")
        data_check_pairs.sort()
        data_check_string = "\n".join(data_check_pairs)

        # Вычисляем секретный ключ из токена бота
        secret_key = hmac.new(
            b"WebAppData", bot_token.encode(), hashlib.sha256
        ).digest()

        # Вычисляем хеш и сравниваем с присланным
        computed_hash = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()

        return computed_hash == received_hash
    except Exception:
        return False


# --- Эндпоинт: главная страница (GET /) ---
# Возвращает HTML-файл — «лицо» нашего приложения
@app.get("/", response_class=HTMLResponse)
async def serve_index() -> HTMLResponse:
    """Отдает index.html — фронтенд Mini App."""
    with open("index.html", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


# --- Эндпоинт: оформление заказа (POST /api/order) ---
# «Официант» принимает заказ и несет его на «кухню»
@app.post("/api/order")
async def create_order(order: Order, request: Request):
    """Обрабатывает заказ: проверяет подпись Telegram и возвращает результат."""
    # Извлекаем initData из заголовка — это «пропуск» от Telegram
    init_data = request.headers.get("X-Telegram-Init-Data", "")

    # Проверяем подпись (если токен не плейсхолдер)
    if BOT_TOKEN != "YOUR_BOT_TOKEN" and init_data:
        if not validate_init_data(init_data, BOT_TOKEN):
            raise HTTPException(
                status_code=403,
                detail="Ошибка безопасности: подпись initData недействительна.",
            )

    return {
        "status": "success",
        "message": f"Заказ на {order.item_name} принят!",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
