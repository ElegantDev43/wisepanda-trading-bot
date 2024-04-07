import telebot
from telebot import types

import config
from src.telegram import start, chains, wallets

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)

commands = [
    types.BotCommand("start", "Main menu"),
    types.BotCommand("chains", "List all supported chains"),
    types.BotCommand("wallets", "List your wallets"),
    types.BotCommand("settings", "Bring up the settings tab"),
    types.BotCommand("orders", "List all pending orders"),
    types.BotCommand("positions", "Overview of all your holdings"),
    types.BotCommand("bots", "List all available backup bots")
]
bot.set_my_commands(commands)

@bot.message_handler(commands=['start'])
def handle_start(message):
    start.handle_start(bot, message)

@bot.message_handler(commands=['chains'])
def handle_chain(message):
    chains.handle_chains(bot, message)

@bot.message_handler(commands=['wallets'])
def handle_wallets(message):
    wallets.handle_wallets(bot, message)

@bot.callback_query_handler(func=lambda _: True)
def handle_callback_query(call):
    if call.data in config.CHAINS:
        chains.handle_select_chain(bot, call.message, call.data)
        return

    if call.data == 'create_wallet':
        wallets.handle_create_wallet(bot, call.message)
    elif call.data == 'import_wallet':
        wallets.handle_import_wallet(bot, call.message)

def start_bot():
    print('\nStarting the bot...')
    bot.infinity_polling(restart_on_change=True)
