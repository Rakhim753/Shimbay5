from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import logging
import os

API_TOKEN = os.getenv("7705891566:AAETdc4uIOJJXDeGPw9jKOiTy-A7SSjkasQ")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Кнопкалар
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    KeyboardButton("🚕 НОКИС ШЫМБАЙ"),
    KeyboardButton("🚕 ШЫМБАЙ НОКИС")
)

# /start командасы
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(
        "Қош келдіңіз! Бағытыңызды таңдаңыз:",
        reply_markup=menu
    )

# НОКИС ШЫМБАЙ кнопкасы
@dp.message_handler(lambda message: message.text == "🚕 НОКИС ШЫМБАЙ")
async def nokis_to_shimbay(message: types.Message):
    await message.answer(
        "Н О К И С Т Е Н\n\n"
        "⤵️⤵️⤵️⤵️⤵️⤵️⤵️\n\n"
        "ШЫМБАЙГА ЖУРЕМИЗ\n\n"
        "АМАНАТ БОЛСА АЛЫП КЕТЕМИЗ\n\n"
        "☎️ +998770149797\n"
        "☎️ +998770149797"
    )

# ШЫМБАЙ НОКИС кнопкасы
@dp.message_handler(lambda message: message.text == "🚕 ШЫМБАЙ НОКИС")
async def shimbay_to_nokis(message: types.Message):
    await message.answer(
        "Ш Ы М Б А Й Д А Н\n\n"
        "⤵️⤵️⤵️⤵️⤵️⤵️⤵️\n\n"
        "НОКИСКЕ ЖУРЕМИЗ\n\n"
        "АМАНАТ БОЛСА АЛЫП КЕТЕМИЗ\n\n"
        "☎️ +998770149797\n"
        "☎️ +998770149797"
    )

# Қалған хабарламалар
@dp.message_handler()
async def echo_message(message: types.Message):
    await message.answer("Хабарыңыз қабылданды. Звонок етиң ☎️")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
