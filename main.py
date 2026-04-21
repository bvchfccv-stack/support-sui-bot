from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 123456789

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

user_state = {}

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🧪 Тест", "💬 Поддержка")

    await msg.answer(
"""🌐 SUI Network | Support & Verification

Добро пожаловать! Вы подключены к системе верификации кошельков SUI Testnet.

Используйте кнопки ниже.""",
        reply_markup=kb
    )

@dp.message_handler(lambda m: m.text == "🧪 Тест")
async def test(msg: types.Message):
    user_state[msg.from_user.id] = "test"

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("⬅ Назад")

    await msg.answer(
"""Отправьте адрес кошелька SUI (0x...)""",
        reply_markup=kb
    )

@dp.message_handler(lambda m: user_state.get(m.from_user.id) == "test")
async def test_input(msg: types.Message):
    if msg.text == "⬅ Назад":
        return await start(msg)

    await msg.answer(
f"""✅ Адрес зарегистрирован:

{msg.text}"""
    )

@dp.message_handler(lambda m: m.text == "💬 Поддержка")
async def support(msg: types.Message):
    user_state[msg.from_user.id] = "support"

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("❌ Завершить диалог")

    await msg.answer("Напишите ваш вопрос", reply_markup=kb)

@dp.message_handler(lambda m: m.text == "❌ Завершить диалог")
async def close(msg: types.Message):
    user_state[msg.from_user.id] = "main"
    await start(msg)

@dp.message_handler()
async def all(msg: types.Message):
    uid = msg.from_user.id

    if user_state.get(uid) == "support":
        await bot.send_message(ADMIN_ID, f"User {uid}: {msg.text}")
        await msg.answer("Отправлено в поддержку")
    else:
        await msg.answer("Нажмите /start")

@dp.message_handler(commands=['reply'])
async def reply(msg: types.Message):
    try:
        _, uid, *text = msg.text.split()
        text = " ".join(text)

        await bot.send_message(uid, f"Support: {text}")
    except:
        await msg.reply("Формат: /reply id текст")

executor.start_polling(dp)
