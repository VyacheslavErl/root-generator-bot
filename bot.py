import telebot
from generate import main_process
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

if not API_TOKEN:
    raise ValueError("API Token not found. Please set TELEGRAM_API_TOKEN in your environment variables.")

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Please enter an English word to generate its root.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    word = message.text.strip()
    
    if not word:
        bot.reply_to(message, "Please enter a valid word.")
        return
    
    response = main_process(word)
    
    if "Error" in response:
        bot.reply_to(message, response, parse_mode='Markdown')
    else:
        bot.reply_to(message, response, parse_mode='Markdown')

if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"An error occurred: {e}")
