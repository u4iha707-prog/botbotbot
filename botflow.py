import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 5585690159

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ===== КЛАВИАТУРА =====
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add("🚀 Клиенты")
kb.add("💼 Возможности")
kb.add("💰 Цена")
kb.add("📩 Связь")
kb.add("📝 Заявка")

user_data = {}

# ===== СТАРТ =====
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Помогаю привлекать клиентов через Telegram 💰\n\n"
        "👇 Выбери:",
        reply_markup=kb
    )

# ===== МЕНЮ =====
@dp.message_handler()
async def menu(message: types.Message):
    user_id = message.from_user.id

    if message.text == "🚀 Клиенты":
        await message.answer(
            "📈 Ты получаешь заявки прямо в Telegram\n"
            "Бот работает за тебя 24/7\n"
            "Ты просто закрываешь клиентов 💰"
        )

    elif message.text == "💼 Возможности":
        await message.answer(
            "💼 Что можно сделать:\n\n"
            "— Приём заявок\n"
            "— Автоответы\n"
            "— Продажи\n"
            "— Запись клиентов"
        )

    elif message.text == "💰 Цена":
        await message.answer(
            "💰 Стоимость:\n\n"
            "— Простой: от 10 000 ₽\n"
            "— Средний: 30 000 ₽\n"
            "— Сложный: от 70 000 ₽\n\n"
            "Напиши — скажу точнее"
        )

    elif message.text == "📩 Связь":
        await message.answer(
            "📩 Связаться:\n\n"
            "Telegram: @saht707\n"
            "📱 +79250345264\n\n"
            "👇 Или оставь заявку"
        )

    elif message.text == "📝 Заявка":
        user_data[user_id] = {"step": "name"}
        await message.answer("✍️ Напиши имя:")

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
                f"🔥 Заявка!\n\n"
                f"Имя: {name}\n"
                f"ID: {user_id}\n"
                f"Задача: {task}"
            )

            await message.answer("✅ Отправлено! Напишу тебе")

            del user_data[user_id]

# ===== ЗАПУСК =====
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)