import telebot
from telebot import types
import json

import config

configuration = {
    'id': 0,
    'wallet': {
        'address': '',
        'private_key': ''
    },
    'active': False,
    'configuration': {
        'max_gas_price': 0,
        'max_gas_limit': 0,
        'slippage': 0,
        'buy': {
            'active': False,
            'buy_price': 0,
            'buy_quantity': 0,
            'min_market_cap': 0,
            'max_market_cap': 0,
            'min_liquidity': 0,
            'max_liquidity': 0,
            'max_buy_tax': 0,
            'gas_delta': 0
        },
        'sell': {
            'active': False,
            'target_price': 0,
            'sell_quantity_at_target': 0,
            'stop_loss': 0,
            'sell_quantity_at_stop_loss': 0,
            'max_sell_tax': 0,
            'gas_delta': 0
        }
    }
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
    bot.send_message(message.chat.id, 'Configuration')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'link':
        bot.send_message(call.message.chat.id, 'You selected Link Wallet')
    elif call.data == 'generate':
        bot.send_message(call.message.chat.id, 'You selected Generate Wallet')

def start():
    bot.polling()