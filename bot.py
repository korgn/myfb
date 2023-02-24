import telebot
import time
from datetime import datetime, timedelta

bot = telebot.TeleBot('6102750853:AAHOZ95KPNLsYKA9AY_D6ef-GJTlBEedG2E')

mute_time = datetime.now() + timedelta(minutes=20)

user_messages = {}

@bot.message_handler(commands=['можливості', 'h'])
def send_help(message):
    bot.send_message(message.chat.id, "Мої можливості досить прості. Я звичайнісенький бот антіспам, без налаштувань чи щось такого, і я мучу за спам, після чого кличу админів командою репорт. \n\n[Розроблено спеціально для чату Бестіарій, і розраховано виключно на працю в ньому.]")
    
@bot.message_handler(['a'])
def send_help(message):
    bot.send_message(message.chat.id, "Мої можливості досить прості. Я звичайнісенький бот антіспам, без налаштувань чи щось такого, і я мучу за спам, після чого кличу админів командою репорт. \n\n[Розроблено спеціально для чату Бестіарій, і розраховано виключно на працю в ньому.]")
    
@bot.message_handler(commands=['suck'])
def send_help(message):
    bot.send_message(message.chat.id, "Смоктати я не вмію, але це гарно робить Ром... Алукард.")
    
    #https://www.youtube.com/watch?v=dQw4w9WgXcQ

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
             bot.restrict_chat_member(message.chat.id, user_id, until_date=mute_time.timestamp())
             #@Did_Non_Stop @dekeractoviy @Rommel_l @wsgf_2014     
             bot.send_message(message.chat.id, f"@Did_Non_Stop, @dekeractoviy - @{username} [{user_id}] був замучений задля припинення спаму.")
           except: 
             bot.send_message(message.chat.id, f"@{username} [{user_id}] повинен був бути замучений, але трапилася помилка, скоріше за усе вона полягає у тому, що цей користувач адміністратор чату.")
           try:
               del user_messages[user_id]
           except:
               pass

bot.polling()
