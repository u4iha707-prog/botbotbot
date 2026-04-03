import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# ================= НАСТРОЙКИ =================
TOKEN = os.getenv("TOKEN")
ADMIN_ID = 5585690159  # <-- твой ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ================= КЛАВИАТУРА =================
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 Получить клиентов")],
        [KeyboardButton(text="💼 Возможности")],
        [KeyboardButton(text="💰 Стоимость")],
        [KeyboardButton(text="📩 Связаться")],
        [KeyboardButton(text="📝 Оставить заявку")]
    ],
    resize_keyboard=True
)

user_data = {}

# ================= СТАРТ =================
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Помогаю привлекать клиентов через Telegram-ботов 💰\n\n"
        "👇 Выбери, что интересно:",
        reply_markup=kb
    )

# ================= ОСНОВНАЯ ЛОГИКА =================
@dp.message()
async def menu(message: types.Message):
    user_id = message.from_user.id

    if message.text == "🚀 Получить клиентов":
        await message.answer(
            "📈 Как это работает:\n\n"
            "Ты получаешь заявки прямо в Telegram\n"
            "Клиенты пишут → бот обрабатывает → ты закрываешь сделки\n\n"
            "💰 Больше клиентов без лишней рутины"
        )

    elif message.text == "💼 Возможности":
        await message.answer(
            "💼 Что можно сделать:\n\n"
            "— Приём заявок\n"
            "— Автоответы\n"
            "— Запись клиентов\n"
            "— Продажи через бота\n\n"
            "📊 Подходит для любого бизнеса"
        )

    elif message.text == "💰 Стоимость":
        await message.answer(
            "💰 Прайс:\n\n"
            "— Простой бот: от 10 000 ₽\n"
            "— Средний: 30 000 – 80 000 ₽\n"
            "— Сложный: от 100 000 ₽\n\n"
            "💬 Напиши задачу — скажу точнее"
        )

    elif message.text == "📩 Связаться":
        await message.answer(
            "📩 Связь:\n\n"
            "📱 Max: +79250345264\n"
            "💬 Telegram: @saht707\n\n"
            "⚡ Отвечаю быстро\n\n"
            "👇 Или оставь заявку"
        )

    elif message.text == "📝 Оставить заявку":
        user_data[user_id] = {"step": "name"}
        await message.answer("✍️ Напиши своё имя:")

    elif user_id in user_data:
        if user_data[user_id]["step"] == "name":
            user_data[user_id]["name"] = message.text
            user_data[user_id]["step"] = "task"
            await message.answer("📋 Опиши задачу:")

        elif user_data[user_id]["step"] == "task":
            name = user_data[user_id]["name"]
            task = message.text

            await bot.send_message(
                ADMIN_ID,
                f"🔥 Новая заявка!\n\n"
                f"👤 Имя: {name}\n"
                f"🆔 ID: {user_id}\n"
                f"📩 Задача: {task}"
            )

            await message.answer("✅ Заявка отправлена! Я скоро напишу тебе")

            del user_data[user_id]

# ================= WEBHOOK =================
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL") + WEBHOOK_PATH

async def on_startup(bot):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(bot):
    await bot.delete_webhook()

def main():
    app = web.Application()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    main()