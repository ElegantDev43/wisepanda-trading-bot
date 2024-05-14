import os
import telebot
from telebot import types

import config
from src.telegram import start, sniper, buyer, orders, positions, bots, hots, seller, limit_order, dca_order
from src.telegram.settings import main as settings, chains, wallets, keyboards

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

commands = [
    types.BotCommand("start", "Main menu"),
    types.BotCommand("hots", "List the 10 hot tokens"),
    types.BotCommand("orders", "List all pending orders"),
    types.BotCommand("positions", "Overview of all your holdings"),
    types.BotCommand("chains", "List all supported chains"),
    types.BotCommand("wallets", "List your wallets"),
    types.BotCommand("settings", "Bring up the settings tab"),
    types.BotCommand("criterias", "Customize your ceriterias"),
    types.BotCommand("keyboards", "Select your trading keys"),
    types.BotCommand("bots", "List all available backup bots")
]
bot.set_my_commands(commands)


@bot.message_handler(commands=['start'])
def handle_start(message):
    start.handle_start(bot, message)


@bot.message_handler(commands=['hots'])
def handle_hots(message):
    hots.handle_hots(bot, message)


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


@bot.message_handler(commands=['keyboards'])
def handle_keyboards(message):
    keyboards.handle_keyboards(bot, message)


@bot.message_handler(commands=['criterias'])
def handle_bots(message):
    bots.handle_bots(bot, message)


@bot.callback_query_handler(func=lambda _: True)
def handle_callback_query(call):
    if call.data == 'start':
        start.handle_start(bot, call.message)
    elif call.data == 'hots':
        hots.handle_hots(bot, call.message)
    elif call.data.startswith('hot '):
        token = call.data[4:]
        call.message.text = token
        buyer.handle_input_token(bot, call.message)
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
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)
    elif call.data == 'chains':
        chains.handle_chains(bot, call.message)
    elif call.data in config.CHAINS:
        chains.handle_select_chain(bot, call.message, call.data)
        # New api
    elif call.data == 'keyboards':
        keyboards.handle_keyboards(bot, call.message)
    elif call.data == 'wallets':
        wallets.handle_wallets(bot, call.message)
    elif call.data in config.ORDERS:
        buyer.handle_select_order(bot, call.message, call.data)
    elif call.data in config.BUY_AMOUNT:
        keyboards.handle_select_buy_amount(bot, call.message, call.data)
    elif call.data in config.GAS_AMOUNT:
        keyboards.handle_select_gas_amount(bot, call.message, call.data)
    elif call.data in config.SELL_AMOUNT:
        keyboards.handle_select_sell_amount(bot, call.message, call.data)
    elif call.data == 'remove_wallet':
        wallets.handle_remove_wallet(bot, call.message)

    elif call.data == 'seller':
        seller.handle_seller(bot, call.message)
    elif call.data == 'sell-limit-orders':
        seller.handle_limit_order(bot, call.message)
    elif call.data == 'sell-market-orders':
        seller.handle_market_order(bot, call.message)
    elif call.data == 'sell-dca-orders':
        seller.handle_dca_order(bot, call.message)

    elif call.data == 'manage-limit-orders':
        limit_order.handle_limit_order(bot, call.message)
    # Market Order
    elif call.data == 'buy-limit-orders':
        buyer.handle_limit_order(bot, call.message)
    elif call.data == 'buy-market-orders':
        buyer.handle_market_order(bot, call.message)
    elif call.data == 'buy-dca-orders':
        buyer.handle_dca_order(bot, call.message)

    elif call.data == 'create_wallet':
        wallets.handle_create_wallet(bot, call.message)
    elif call.data == 'import_wallet':
        wallets.handle_import_wallet(bot, call.message)

    elif call.data.startswith('auto wallet '):
        sniper.handle_toggle_wallet(bot, call.message, call.data[12:])
    elif call.data.startswith('auto buy '):
        amount = call.data[9:]
        if amount == 'x':
            sniper.handle_buy_x(bot, call.message)
        else:
            amount = float(amount)
            sniper.handle_buy(bot, call.message, amount)
    elif call.data.startswith('manual wallet '):
        buyer.handle_toggle_wallet(bot, call.message, call.data[14:])
    elif call.data == 'make order':
        buyer.handle_buy(bot, call.message)
    elif call.data.startswith('buy amount'):
        amount = call.data[11:]
        if amount == 'x':
            buyer.handle_buy_x(bot, call.message)
        else:
            amount = float(amount)
            buyer.handle_buy_amount(bot, call.message, amount)


def initialize():
    print('Starting the bot...')
    bot.infinity_polling(restart_on_change=True)
