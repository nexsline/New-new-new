import os
import asyncio
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import logging

# === НАСТРОЙКИ ===
TOKEN = os.environ.get("TOKEN")               # токен от BotFather
USER_ID = int(os.environ.get("USER_ID"))      # твой Telegram ID (число)
URL = os.environ.get("URL")                   # ссылка на товар
CHECK_INTERVAL = 300                          # интервал проверки в секундах (5 минут)

logging.basicConfig(level=logging.INFO)

# Создание бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция проверки наличия товара
async def check_stock():
    while True:
        try:
            response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")
            button = soup.find("button", {"data-testid": "add-to-cart-button"})
            if button and "нет в наличии" not in button.text.lower():
                await bot.send_message(USER_ID, f"✅ Товар появился в наличии!\n{URL}")
            else:
                print("❌ Пока нет в наличии.")
        except Exception as e:
            print(f"⚠️ Ошибка при проверке: {e}")
        await asyncio.sleep(CHECK_INTERVAL)

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 Привет! Я слежу за твоим товаром и напишу, когда он появится 🔔")

# Запуск проверки при старте
async def on_startup():
    asyncio.create_task(check_stock())

# Главная функция запуска бота
async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())