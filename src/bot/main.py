import telebot
from telebot import types

import config
from src.bot import start, chain, wallet

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)

commands = [
    types.BotCommand("start", "Start the bot"),
    types.BotCommand("chain", "Configure the chain setting"),
    types.BotCommand("wallet", "Configure the wallet setting")
]
bot.set_my_commands(commands)

@bot.message_handler(commands=['start'])
def handle_start(message):
    start.handle_start(bot, message)

@bot.message_handler(commands=['chain'])
def handle_chain(message):
    chain.handle_chain(bot, message)

@bot.message_handler(commands=['wallet'])
def handle_wallet(message):
    wallet.handle_wallet(bot, message)

@bot.callback_query_handler(func=lambda _: True)
def handle_callback_query(call):
    if call.data in config.CHAINS:
        chain.handle_select_chain(bot, call.message, call.data)
        return

    if call.data == 'create_wallet':
        wallet.handle_create_wallet(bot, call.message)
    elif call.data == 'import_wallet':
        wallet.handle_import_wallet(bot, call.message)

def start_bot():
    print('\nStarting bot...')
    bot.infinity_polling(restart_on_change=True)
