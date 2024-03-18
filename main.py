import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, 'Welcome to Wise Panda Trading Bot!')

@bot.message_handler(commands=['sniper'])
def handle_start(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton('Link Wallet', callback_data='option1'),
        types.InlineKeyboardButton('Generate Wallet', callback_data='option2')
    )
    bot.send_message(message.chat.id, 'Please choose an option:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'option1':
        bot.answer_callback_query(call.id, 'You chose Option 1')
    elif call.data == 'option2':
        bot.answer_callback_query(call.id, 'You chose Option 2')

bot.polling()