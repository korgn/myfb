import time
import telegram
import os
PORT = int(os.environ.get('PORT', 5000))

bot = telegram.Bot(token='6102750853:AAHOZ95KPNLsYKA9AY_D6ef-GJTlBEedG2E')
TOKEN = '6102750853:AAHOZ95KPNLsYKA9AY_D6ef-GJTlBEedG2E'

user_messages = {}

def send_help(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, "Мої можливості досить прості. Я звичайнісенький бот антіспам, без налаштувань чи щось такого, і я мучу за спам, після чого кличу админів командою репорт. \n\n[Розроблено спеціально для чату Бестіарій, і розраховано виключно на працю в ньому.]")

def smoktat(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, "Смоктати я не вмію, але це гарно робить Ром... Алукард.")
    
    #https://www.youtube.com/watch?v=dQw4w9WgXcQ

def handle_message(update, context):
    message = update.message
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
                context.bot.restrict_chat_member(chat_id, user_id, until_date=0)
                context.bot.send_message(chat_id, f"@{username}({user_id}) замучений назавжди")
                context.bot.send_message(chat_id, f"/report @{username} [{user_id}] був замучений задля припинення спаму, дії далі вирішите самі.")
            except: 
                context.bot.send_message(chat_id, f"Помилка, скоріше за усе вона полягає в тому, що спамить адмін.")
            try:
                del user_messages[user_id]
            except:
                pass

from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

updater = Updater(token='your_bot_token_here', use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler(['можливості', 'h'], send_help))
dispatcher.add_handler(CommandHandler('s', smoktat))
dispatcher.add_handler(MessageHandler(Filters.text | Filters.animation | Filters.sticker, handle_message))
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members,))

updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
updater.bot.setWebhook('https://yourherokuappname.herokuapp.com/' + TOKEN)
updater.idle()
