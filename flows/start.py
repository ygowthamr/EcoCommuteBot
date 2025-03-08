import sys
sys.path.append("..")

from cred.cred import bot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🚘 Offer a Ride"), KeyboardButton("👤 Find a Ride"))
    bot.send_message(
        chat_id,
        f"**Welcome, {message.from_user.first_name}!** 🚗\n"
        "🤖 **EcoCommute Bot** is here to help you find the perfect ride.\n"
        "👉 Choose an option below to get started:",
        parse_mode="Markdown",
        reply_markup=markup
    )
