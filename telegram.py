import telebot
from telebot import types
import json

import config
import db

configuration = {
    'id': 0,
    'wallet': {
        'address': '0xa69876a83E11f778B2c7492f02b606bf2BBe52a8',
        'private_key': '08b17887d76a90941c0ab920b585a4c7a578235138a8d3e483e494e17cbabc19'
    },
    'active': True,
    'configuration': {
        'max_gas_price': 0,
        'max_gas_limit': 0,
        'slippage': 0,
        'buy': {
            'active': True,
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
            'active': True,
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
    id = message.chat.id

    if db.exist(id) == False:
        db.create(id)

    keyboard = types.InlineKeyboardMarkup()
    connect_button = types.InlineKeyboardButton('Connect Wallet', callback_data='connect')
    sniper_button = types.InlineKeyboardButton('Sniper Bot', callback_data='sniper')
    keyboard.add(connect_button)
    keyboard.add(sniper_button)

    bot.send_message(id, 'Welcome to Wise Panda Trading Bot!', reply_markup=keyboard)

@bot.message_handler(commands=['connect'])
def handle_connect(message):
    id = message.chat.id

    user = db.get(id)

    keyboard = types.InlineKeyboardMarkup()
    connect_button = types.InlineKeyboardButton('Link Wallet', callback_data='link')
    sniper_button = types.InlineKeyboardButton('Generate Wallet', callback_data='generate')
    keyboard.add(connect_button)
    keyboard.add(sniper_button)

    bot.send_message(id, json.dumps(user.wallet, indent=4), reply_markup=keyboard)

@bot.message_handler(commands=['link'])
def handle_link(message):
    return

@bot.message_handler(commands=['generate'])
def handle_generate(message):
    return

@bot.message_handler(commands=['sniper'])
def handle_sniper(message):
    bot.send_message(message.chat.id, 'Configuration')

@bot.message_handler(commands=['configure'])
def handle_configure(message):
    return

@bot.message_handler(commands=['activate'])
def handle_activate(message):
    return

@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    return

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'connect':
        handle_connect(call.message)
    elif call.data == 'link':
        handle_link(call.message)
    elif call.data == 'generate':
        handle_generate(call.message)
    elif call.data == 'sniper':
        handle_sniper(call.message)
    elif call.data == 'configure':
        handle_configure(call.message)
    elif call.data == 'activate':
        handle_activate(call.message)
    elif call.data == 'cancel':
        handle_cancel(call.message)

def start():
    bot.polling()