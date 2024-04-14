import os
import telebot
from telebot import types

import config
from src.telegram import start, sniper, buyer, orders, positions, bots
from src.telegram.settings import main as settings, chains, wallets

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

commands = [
    types.BotCommand("start", "Main menu"),
    types.BotCommand("orders", "List all pending orders"),
    types.BotCommand("positions", "Overview of all your holdings"),
    types.BotCommand("chains", "List all supported chains"),
    types.BotCommand("wallets", "List your wallets"),
    types.BotCommand("settings", "Bring up the settings tab"),
    types.BotCommand("bots", "List all available backup bots")
]
bot.set_my_commands(commands)

@bot.message_handler(commands=['start'])
def handle_start(message):
    start.handle_start(bot, message)

@bot.message_handler(commands=['orders'])
def handle_orders(message):
    orders.handle_orders(bot, message)

@bot.message_handler(commands=['positions'])
def handle_positions(message):
    positions.handle_positions(bot, message)

@bot.message_handler(commands=['chains'])
def handle_chain(message):
    chains.handle_chains(bot, message)

@bot.message_handler(commands=['wallets'])
def handle_wallets(message):
    wallets.handle_wallets(bot, message)

@bot.message_handler(commands=['settings'])
def handle_settings(message):
    settings.handle_settings(bot, message)

@bot.message_handler(commands=['bots'])
def handle_bots(message):
    bots.handle_bots(bot, message)

@bot.callback_query_handler(func=lambda _: True)
def handle_callback_query(call):
    if call.data == 'start':
        start.handle_start(bot, call.message)
    elif call.data == 'sniper':
        sniper.handle_sniper(bot, call.message)
    elif call.data == 'buyer':
        buyer.handle_buyer(bot, call.message)
    elif call.data == 'orders':
        orders.handle_orders(bot, call.message)
    elif call.data == 'positions':
        positions.handle_positions(bot, call.message)
    elif call.data == 'settings':
        settings.handle_settings(bot, call.message)
    elif call.data == 'bots':
        bots.handle_bots(bot, call.message)
    elif call.data == 'close':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'chains':
        chains.handle_chains(bot, call.message)
    elif call.data == 'wallets':
        wallets.handle_wallets(bot, call.message)
    elif call.data in config.CHAINS:
        chains.handle_select_chain(bot, call.message, call.data)
    elif call.data == 'create_wallet':
        wallets.handle_create_wallet(bot, call.message)
    elif call.data == 'import_wallet':
        wallets.handle_import_wallet(bot, call.message)
    elif call.data.startswith('auto wallet '):
        sniper.handle_toggle_wallet(bot, call.message, call.data[12:])

def initialize():
    print('Starting the bot...')
    bot.infinity_polling(restart_on_change=True)
