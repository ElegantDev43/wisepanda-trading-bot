import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)

configure_requests = {}  # Dictionary to store configuration requests

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, 'Welcome to Wise Panda Trading Bot!')

@bot.message_handler(commands=['connect'])
def handle_connect(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton('Link Wallet', callback_data='link'),
        types.InlineKeyboardButton('Generate Wallet', callback_data='generate')
    )
    bot.send_message(message.chat.id, 'Please choose an option:', reply_markup=keyboard)

@bot.message_handler(commands=['configure'])
def handle_configure(message):
    # Ask for configuration details
    bot.send_message(message.chat.id, 'Please enter your configuration details:')
    # Register next message as configuration input
    bot.register_next_step_handler(message, process_configure)

def process_configure(message):
    # Store configuration request
    configure_requests[message.chat.id] = message.text
    bot.send_message(message.chat.id, 'Configuration saved successfully.')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'link':
        bot.send_message(call.message.chat.id, 'You selected Link Wallet')
    elif call.data == 'generate':
        bot.send_message(call.message.chat.id, 'You selected Generate Wallet')

# Start polling
bot.polling()