import asyncio
import time
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode

API_TOKEN = '6102750853:AAHOZ95KPNLsYKA9AY_D6ef-GJTlBEedG2E'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_messages = {}

@dp.message_handler(commands=['h'])
@dp.message_handler(commands=['можливості'])
async def send_help(message: types.Message):
    await bot.send_message(message.chat.id, "Мої можливості досить прості. Я звичайнісенький бот антіспам, без налаштувань чи щось такого, і я мучу за спам, після чого кличу админів командою репорт. \n\n[Розроблено спеціально для чату Бестіарій, і розраховано виключно на працю в ньому.]")

@dp.message_handler(commands=['s'])
async def send_help(message: types.Message):
    await bot.send_message(message.chat.id, "Смоктати я не вмію, але це гарно робить Ром... Алукард.\n\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ")

@dp.message_handler(content_types=['text', 'animation', 'sticker'])
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    if message.forward_from:
        return

    if user_id not in user_messages:
        user_messages[user_id] = []

    user_messages[user_id].append(time.time())

    if len(user_messages[user_id]) >= 5:
        if user_messages[user_id][-1] - user_messages[user_id][-3] <= 5:
            try:
                await bot.restrict_chat_member(message.chat.id, user_id, until_date=0)
                await bot.send_message(message.chat.id, f"@{username}({user_id}) замучений назавжди")
                await bot.send_message(message.chat.id, f"/report @{username} [{user_id}] був замучений задля припинення спаму, дії далі вирішите самі.")
            except:
                await bot.send_message(message.chat.id, f"Помилка, скоріше за усе вона полягає в тому, що спамить адмін.")
            try:
                del user_messages[user_id]
            except:
                pass

@dp.message_handler(content_types=['new_chat_members'])
async def handle_new_chat_member(message: types.Message):
    await bot.send_message(message.chat.id, f"Привіт, @{message.new_chat_members[0].username}!")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    asyncio.run(dp.start_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=API_TOKEN,
        webhook_url=f"https://myfb.com/{API_TOKEN}"
    ))
