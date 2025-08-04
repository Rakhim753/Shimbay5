import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

API_TOKEN = "7705891566:AAETdc4uIOJJXDeGPw9jKOiTy-A7SSjkasQ"
ADMIN_ID = 7398183328

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 🧠 Стейт машиналары
class OrderStates(StatesGroup):
    waiting_for_location = State()
    waiting_for_contact = State()

# 📊 Пайдаланушылар базасы (жәй сақтаймыз)
users_set = set()

@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    users_set.add(message.from_user.id)

    # 🔔 Жаңа қолданушы админге хабарланады
    if message.from_user.id != ADMIN_ID:
        await bot.send_message(
            ADMIN_ID,
            f"👤 ЖАҢА ПАЙДАЛАНЫУЩЫ:\n"
            f"🆔 {message.from_user.id}\n"
            f"👤 Аты: {message.from_user.full_name}\n"
            f"🔗 Username: @{message.from_user.username or 'жоқ'}"
        )

    text = (
        "🚖 ШЫМБАЙ-НУКУС ТАКСИ 🚖\n\n"
        "📍 БИЗДИҢ МАРШРУТЛАРЫМЫЗ\n\n"
        "↗️ ШЫМБАЙДАН ➡️ НУКУСГЕ\n"
        "↙️ НУКУСТЕН ⬅️ ШЫМБАЙҒА\n\n"
        "🚖 Басқа қалаларға да хызмет көрсетемиз:\n"
        "• ТЕК ҒАНА БУЙЫРТПА АРҚАЛЫ\n\n"
        "📞 +998770149797\n📞 +998770149797\n\n"
        "👨‍💻 АДМИН:@rakhim753\n\n"
        "Төмендеги кнопкалардан өзиңизге кереклисин таңлаң! 😊"
    )

    buttons = [
        [KeyboardButton(text="🚗 ШЫМБАЙ ➡️ НӨКІС")],
        [KeyboardButton(text="🚕 НӨКІС ➡️ ШЫМБАЙ")]
    ]
    # 🔒 Тек админге арналған статистика кнопкасы
    if message.from_user.id == ADMIN_ID:
        buttons.append([KeyboardButton(text="📊 Статистика")])

    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await state.clear()
    await message.answer(text, reply_markup=markup)

@dp.message(F.text == "📊 Статистика")
async def stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    total_users = len(users_set)
    await message.answer(f"📊 Ботқа қосылған адамлар саны: {total_users} 👥")

@dp.message(F.text == "🚗 ШЫМБАЙ ➡️ НӨКІС")
@dp.message(F.text == "🚕 НӨКІС ➡️ ШЫМБАЙ")
async def direction_chosen(message: types.Message, state: FSMContext):
    direction = message.text
    await state.update_data(direction=direction)

    location_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 МӘНЗИЛИМДИ ЖИБЕРИУ", request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await state.set_state(OrderStates.waiting_for_location)
    await message.answer("📍 МӘНЗИЛИҢИЗДИ ЖИБЕРИҢ:", reply_markup=location_kb)

@dp.message(OrderStates.waiting_for_location, F.location)
async def get_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.location)

    contact_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📞 Нөмеримди жибериу", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await state.set_state(OrderStates.waiting_for_contact)
    await message.answer("📞 Енді телефон нөміріңізді жіберің:", reply_markup=contact_kb)

@dp.message(OrderStates.waiting_for_contact, F.contact)
async def get_contact(message: types.Message, state: FSMContext):
    data = await state.get_data()
    location = data.get("location")
    direction = data.get("direction", "Белгісіз")
    contact = message.contact

    text = (
        "📥 ЖАҢА БУЙЫРТПА:\n\n"
        f"🗺МӘНЗИЛ: {direction}\n"
        f"👤 Аты: {message.from_user.full_name}\n"
        f"🆔 ID: {message.from_user.id}\n"
        f"📞 Тел: {contact.phone_number}\n"
        f"📍 Локация: https://maps.google.com/?q={location.latitude},{location.longitude}\n"
        f"👤 Username: @{message.from_user.username or 'жоқ'}"
    )

    await bot.send_message(ADMIN_ID, text)
    await message.answer(
        "✅ Т БУЙЫРТПАҢЫЗ  ҚАБЫЛЛАНДЫn"
        "🚖 ТЕЗ АРАДА БАЙЛАНЫСАМЫЗ",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()

# 🤖 Басқа хабарламалар
@dp.message()
async def fallback(message: types.Message):
    await message.answer("🚖 БУЙРТПА БЕРИУ УШЫН /start ТЫ БАСЫҢ.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
