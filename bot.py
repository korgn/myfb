import telebot
import time
from telebot import types
from datetime import datetime, timedelta

bot = telebot.TeleBot('6102750853:AAHOZ95KPNLsYKA9AY_D6ef-GJTlBEedG2E')

mute_time = datetime.now() + timedelta(minutes=20)

user_messages = {}

@bot.message_handler(commands=['можливості', 'h'])
def send_help(message):
    bot.send_message(message.chat.id, "Мої можливості досить прості. Я звичайнісенький бот антіспам, без налаштувань чи щось такого, і я мучу за спам, після чого кличу админів командою репорт. \n\n[Розроблено спеціально для чату Бестіарій, і розраховано виключно на працю в ньому.]\n \nбот BAS(Bestiariy AntiSpam) версії 0.3")
    
@bot.message_handler(commands=['suck'])
def send_help(message):
    bot.send_message(message.chat.id, "Алукард смокче член.")

@bot.message_handler(content_types=['text', 'animation', 'sticker'])
def handle_message(message):
    user_id = message.from_user.id
    username = message.from_user.username

    if message.forward_from:
        return

    if user_id not in user_messages:
        user_messages[user_id] = []

    user_messages[user_id].append(time.time())

    if len(user_messages[user_id]) >= 5:
        if user_messages[user_id][-1] - user_messages[user_id][-5] <= 5:
            try:
                bot.restrict_chat_member(message.chat.id, user_id, until_date=mute_time)
                bot.send_message(message.chat.id, f"@{username} [{user_id}] був замучений задля припинення спаму.", reply_markup=create_keyboard(user_id))
            except: 
                bot.send_message(message.chat.id, f"@{username} [{user_id}] повинен був бути замучений, але трапилася помилка, скоріше за усе вона полягає у тому, що цей користувач адміністратор чату.")

            try:
                del user_messages[user_id]
            except:
                pass

def create_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup()
    ban_button = types.InlineKeyboardButton("Бан", callback_data=f"ban_{user_id}")
    unmute_button = types.InlineKeyboardButton("Розмут", callback_data=f"unmute_{user_id}")
    keyboard.add(ban_button, unmute_button)
    return keyboard

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.data.split("_")[1]
    if call.from_user.id != 1149042468 or 770662069 or 1380896061: # replace with the ID of the chat administrator
        return
    if call.data.startswith("ban"):
        bot.kick_chat_member(call.message.chat.id, user_id)
    elif call.data.startswith("unmute"):
        bot.restrict_chat_member(call.message.chat.id, user_id, can_send_messages=True)
    bot.answer_callback_query(call.id)

bot.polling()
