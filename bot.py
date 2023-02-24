import telebot
import time
from telebot import types
from datetime import datetime, timedelta

bot = telebot.TeleBot('6102750853:AAHOZ95KPNLsYKA9AY_D6ef-GJTlBEedG2E')

mute_time = datetime.now() + timedelta(minutes=20)

user_messages = {}

@bot.message_handler(commands=['можливості', 'h'])
def send_help(message):
    bot.send_message(message.chat.id, "Мої можливості досить прості. Я звичайнісенький бот антіспам, без налаштувань чи щось такого, і я мучу за спам, після чого кличу админів командою репорт. \n\n[Розроблено спеціально для чату Бестіарій, і розраховано виключно на працю в ньому.]\n \n бот BAS(Bestiariy AntiSpam) версії 0.3")
    
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
                # Заборонити користувача на 5 хвилин
                bot.restrict_chat_member(message.chat.id, user_id, until_date=0)

                # Створення кнопок для зняття муту та бану, якщо користувач - адміністратор, не створювати кнопки
                if bot.get_chat_member(message.chat.id, user_id).status != "administrator":
                    markup = types.InlineKeyboardMarkup(row_width=2)
                    unmute_button = types.InlineKeyboardButton("Зняти мут", callback_data=f"unmute:{user_id}")
                    ban_button = types.InlineKeyboardButton("Забанити", callback_data=f"ban:{user_id}")
                    markup.add(unmute_button, ban_button)
                else:
                    markup = None

                # Відправлення повідомлення про мут та кнопок для зняття муту та бану
                bot.send_message(message.chat.id, f"@{username} [{user_id}] був замучений задля припинення спаму.", reply_markup=markup)
            except: 
                bot.send_message(message.chat.id, f"@{username} [{user_id}] повинен був бути замучений, але трапилася опимлка, скоріше за усе вона полягає у тому, що цей користувач адміністратор чату.")
            try:
                del user_messages[user_id]
            except:
                pass

# Обробник натиснення кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.data.split(":")[1]

    if call.data.startswith("unmute"):
        # Зняти мут з користувача
        bot.restrict_chat_member(call.message.chat.id, user_id, until_date=0, can_send_messages=True)
        bot.answer_callback_query(call.id, text="Мут знято")
    elif call.data.startswith("ban"):
        # Забанити користувача
        bot.ban_chat_member(call.message.chat.id, user_id)
        bot.answer_callback_query(call.id, text="Користувач забанений")


bot.polling()
