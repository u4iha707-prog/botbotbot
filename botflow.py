import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 5585690159

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}

# Кнопки
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 Получить клиентов")],
        [KeyboardButton(text="💼 Возможности")],
        [KeyboardButton(text="💰 Стоимость")],
        [KeyboardButton(text="📩 Связаться")],
        [KeyboardButton(text="🔥 Оставить заявку")]
    ],
    resize_keyboard=True
)

# Старт
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет!\n\n"
        "🚀 Хочешь получать клиентов через Telegram автоматически?\n\n"
        "🤖 Я создаю ботов, которые:\n"
        "— принимают заявки 24/7\n"
        "— увеличивают продажи\n"
        "— экономят время\n\n"
        "👇 Выбери ниже или оставь заявку",
        reply_markup=kb
    )

# Основная логика
@dp.message()
async def menu(message: types.Message):
    user_id = message.from_user.id

    if message.text == "🚀 Получить клиентов":
        await message.answer(
            "🔥 Представь:\n\n"
            "Клиенты сами пишут тебе\n"
            "Бот отвечает за тебя\n"
            "Ты просто получаешь заявки 💰\n\n"
            "👇 Хочешь так же? Нажми «Оставить заявку»"
        )

    elif message.text == "💼 Возможности":
        await message.answer(
            "🤖 Возможности бота:\n\n"
            "— Приём заявок 24/7\n"
            "— Автоответы клиентам\n"
            "— Запись и обработка заявок\n"
            "— Продажи через Telegram\n\n"
            "🚀 Всё работает автоматически"
        )

    elif message.text == "💰 Стоимость":
        await message.answer(
            "💰 Сколько стоит бот?\n\n"
            "— Базовый: от 10 000 ₽\n"
            "— Для бизнеса: 30 000 – 80 000 ₽\n"
            "— Под ключ: от 100 000 ₽\n\n"
            "🔥 Подберу вариант под твой бюджет\n"
            "👇 Оставь заявку и скажу точную цену"
        )

    elif message.text == "📩 Связаться":
        await message.answer(
            "📩 Связаться со мной:\n\n"
            "📱 Max Messenger: +79250345264\n"
            "💬 Telegram: @saht707\n\n"
   	    "⚡ Отвечаю быстро\n\n"
   	    "👇 Или оставь заявку — напишу сам"
        )

    # ЗАЯВКА
    elif message.text == "🔥 Оставить заявку":
        user_data[user_id] = {"step": "name"}
        await message.answer("✍️ Напиши своё имя:")

    elif user_id in user_data:

        if user_data[user_id]["step"] == "name":
            user_data[user_id]["name"] = message.text
            user_data[user_id]["step"] = "contact"
            await message.answer("📱 Оставь свой Telegram или WhatsApp:")

        elif user_data[user_id]["step"] == "contact":
            user_data[user_id]["contact"] = message.text
            user_data[user_id]["step"] = "request"
            await message.answer("📋 Опиши задачу:")

        elif user_data[user_id]["step"] == "request":
            name = user_data[user_id]["name"]
            contact = user_data[user_id]["contact"]
            request = message.text

            text = (
                f"🔥 Новая заявка!\n\n"
                f"👤 Имя: {name}\n"
                f"📱 Контакт: {contact}\n"
                f"🆔 ID: {user_id}\n"
                f"📩 Запрос: {request}"
            )

            await bot.send_message(ADMIN_ID, text)

            await message.answer(
                "✅ Готово!\n\n"
                "Я получил заявку и скоро напишу тебе 👌"
            )

            del user_data[user_id]

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())