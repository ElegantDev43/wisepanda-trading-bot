import telebot
from telebot import types
import json

import config

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

users = []


bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    users.append({id: message.chat.id})
    print(message.chat.id)
    bot.reply_to(message, 'Welcome to Wise Panda Trading Bot!')

@bot.message_handler(commands=['configure'])
def handle_configure(message):
    bot.send_message(message.chat.id, 'Configuration')

@bot.message_handler(commands=['activate'])
def handle_configure(message):
    bot.send_message(message.chat.id, 'Configuration')

def start():
    bot.polling()