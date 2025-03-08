import telebot
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("API_KEY") 

bot = telebot.TeleBot(TOKEN)
