import telebot
from telebot import types

import config

configure = {
    'max_gas_price': None,
    'max_gas_limit': None,
    'slippage': None
}

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)

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
    bot.send_message(message.chat.id, 'Please enter your configuration details:')
    bot.send_message(message.chat.id, 'Enter max gas price:')
    bot.register_next_step_handler(message, process_max_gas_price)

def process_max_gas_price(message):
    try:
        max_gas_price = int(message.text)
        configure['max_gas_price'] = max_gas_price
        bot.send_message(message.chat.id, 'Enter max gas limit:')
        bot.register_next_step_handler(message, process_max_gas_limit)
    except Exception as e:
        bot.send_message(message.chat.id, f'Error: {str(e)}')

def process_max_gas_limit(message):
    try:
        max_gas_limit = int(message.text)
        configure['max_gas_limit'] = max_gas_limit
        bot.send_message(message.chat.id, 'Enter slippage:')
        bot.register_next_step_handler(message, process_slippage)
    except Exception as e:
        bot.send_message(message.chat.id, f'Error: {str(e)}')

def process_slippage(message):
    try:
        slippage = message.text
        configure['slippage'] = slippage
        bot.send_message(message.chat.id, 'Configuration saved successfully.')
    except Exception as e:
        bot.send_message(message.chat.id, f'Error: {str(e)}')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'link':
        bot.send_message(call.message.chat.id, 'You selected Link Wallet')
    elif call.data == 'generate':
        bot.send_message(call.message.chat.id, 'You selected Generate Wallet')

bot.polling()