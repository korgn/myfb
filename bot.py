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

@bot.message_handler(commands=['bot'])
def send_help(message):
    fchid = -1001863999290
    fmesid = 20
    bot.forward_message(message.chat.id, fchid, fmesid, disable_notification=True)
    
@bot.message_handler(commands=['porno'])
def send_help(message):
    fchid = -1001863999290
    fmesid = 50
    bot.forward_message(message.chat.id, fchid, fmesid, disable_notification=True)
    
@bot.message_handler(commands=['koks'])
def send_help(message):
    fchid = -1001863999290
    fmesid = 21
    bot.forward_message(message.chat.id, fchid, fmesid, disable_notification=True)
    
@bot.message_handler(commands=['ебанута'])
def send_help(message):
    fchid = -1001863999290
    fmesid = 47
    bot.forward_message(message.chat.id, fchid, fmesid, disable_notification=True)
    
@bot.message_handler(commands=['нормальна'])
def send_help(message):
    fchid = -1001863999290
    fmesid = 48
    bot.forward_message(message.chat.id, fchid, fmesid, disable_notification=True)
    
@bot.message_handler(commands=['бухий'])
def send_help(message):
    fchid = -1001863999290
    fmesid = 35
    bot.forward_message(message.chat.id, fchid, fmesid, disable_notification=True)
    
@bot.message_handler(commands=['СС'])
def send_help(message):
    fchid = -1001863999290
    fmesid = 51
    bot.forward_message(message.chat.id, fchid, fmesid, disable_notification=True)
    
@bot.message_handler(commands=['Odesa'])
def send_help(message):
    fchid = -1001863999290
    fmesid = 24
    bot.forward_message(message.chat.id, fchid, fmesid, disable_notification=True)

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
            # перевірити, чи користувач вже в муті
            member = bot.get_chat_member(message.chat.id, user_id)
            if member.status == "restricted":
                return

            try:
                bot.restrict_chat_member(message.chat.id, user_id, until_date=mute_time)
                bot.send_message(message.chat.id, f"@dekeractoviy - @{username} [{user_id}] був замучений задля припинення спаму.", reply_markup=create_keyboard(user_id))
            except:
                bot.send_message(message.chat.id, f"@{username} [{user_id}] повинен був бути замучений, але трапилася помилка, скоріше за усе вона полягає у тому, що цей користувач адміністратор чату.")

            user_messages.pop(user_id, None)


def create_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup()
    ban_button = types.InlineKeyboardButton("Бан", callback_data=f"ban_{user_id}")
    unmute_button = types.InlineKeyboardButton("Розмут", callback_data=f"unmute_{user_id}")
    keyboard.add(ban_button, unmute_button)
    return keyboard

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.data.split("_")[1]
    admins = [1149042468, 770662069, 1380896061] # replace with the IDs of the chat administrators

    if call.from_user.id not in admins:
        return

    if call.data.startswith("ban"):
        bot.kick_chat_member(call.message.chat.id, user_id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"[{user_id}] був забанений.")
    elif call.data.startswith("unmute"):
        bot.restrict_chat_member(chat_id=call.message.chat.id, user_id=user_id, can_send_messages=True, can_send_other_messages=True)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"[{user_id}] був розмучений.")

    bot.answer_callback_query(call.id)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)


bot.polling()

