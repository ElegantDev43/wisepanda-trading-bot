import telebot
from telebot import types

from web3 import Web3
import json

import config

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, 'Welcome to Wise Panda Trading Bot!')

@bot.message_handler(commands=['sniper'])
def handle_sniper(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton('Link Wallet', callback_data='link'),
        types.InlineKeyboardButton('Generate Wallet', callback_data='generate')
    )
    bot.send_message(message.chat.id, 'Please choose an option:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'link':
        bot.answer_callback_query(call.id, 'Link')
    elif call.data == 'generate':
        bot.answer_callback_query(call.id, 'Generate')

@bot.message_handler(commands=['buy'])
def handle_buy(message):
    bot.reply_to(message, 'Buy')

bot.polling()