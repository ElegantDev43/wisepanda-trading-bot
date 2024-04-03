import telebot
from telebot import types
import json
import threading

import src.config as config
import src.database as database
import src.sniper as sniper

thread_flags = {}

input_wallet = {
    'chain': None,
    'address': None,
    'private_key': None
}

input_configuration = {
    'symbol': None,
    'max_gas_price': None,
    'max_gas_limit': None,
    'slippage': None
}

input_buy = {
    'buy_price': None,
    'buy_quantity': None,
    'min_market_cap': None,
    'max_market_cap': None,
    'min_liquidity': None,
    'max_liquidity': None,
    'max_buy_tax': None,
    'gas_delta': None
}

input_sell = {
    'target_price': None,
    'sell_quantity_at_target': None,
    'stop_loss': None,
    'sell_quantity_at_stop_loss': None,
    'max_sell_tax': None,
    'gas_delta': None
}

def process_inputs(id, current, target):
    keys = list(current.keys())
    if len(keys) > 0:
        key = keys[0]
        bot.send_message(id, f'Enter {key.replace('_', ' ')}:')
        bot.register_next_step_handler_by_chat_id(id, lambda message: process_input(id, message, key, current, target))
    else:
        if target == input_wallet:
            database.update_user(id, 'wallets', input_wallet)
            bot.send_message(id, 'Saved successfully.')
            bot.send_message(id, json.dumps(input_wallet, indent=4))
        elif target == input_configuration:
            bot.send_message(id, 'Please enter buy details')
            process_inputs(id, input_buy, input_buy)
        elif target == input_buy:
            bot.send_message(id, 'Please enter sell details')
            process_inputs(id, input_sell, input_sell)
        elif target == input_sell:
            configuration = {
                **input_configuration,
                'buy': input_buy,
                'sell': input_sell
            }
            database.update_user(id, 'configuration', configuration)
            bot.send_message(id, 'Saved successfully.')
            bot.send_message(id, json.dumps(configuration, indent=4))

def process_input(id, message, currentKey, current, target):
    target[currentKey] = message.text
    current = {key: value for key, value in current.items() if key != currentKey}
    process_inputs(id, current, target)

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    database.create_user(message.chat.id)

    text = '''
*Welcome to Wise Panda Trading Bot!*

[Visit our Official Chat](https://t.me/wisepandaofficial)

[Visit our Website](https://www.wisepanda.ai)
    '''
    keyboard = types.InlineKeyboardMarkup()
    connect_button = types.InlineKeyboardButton('Connect Wallet', callback_data='connect')
    sniper_button = types.InlineKeyboardButton('Sniper Bot', callback_data='sniper')
    keyboard.add(connect_button)
    keyboard.add(sniper_button)
    bot.send_message(message.chat.id, text, parse_mode='Markdown', disable_web_page_preview=True, reply_markup=keyboard)

@bot.message_handler(commands=['chains'])
def handle_chains(message):
    text = '''
*Settings > Chains*
    
Select the chain you'd like to use. You can only have one chain selected at the same time. Your defaults and presets will be different for each chain.
    '''
    keyboard = types.InlineKeyboardMarkup()
    ethereum_button = types.InlineKeyboardButton(text="ethereum", callback_data="ethereum")
    bsc_button = types.InlineKeyboardButton(text="bsc", callback_data="bsc")
    solana_button = types.InlineKeyboardButton(text="solana", callback_data="solana")
    tron_button = types.InlineKeyboardButton(text="tron", callback_data="tron")
    cardano_button = types.InlineKeyboardButton(text="cardano", callback_data="cardano")
    keyboard.row(ethereum_button)
    keyboard.row(bsc_button)
    keyboard.row(solana_button)
    keyboard.row(tron_button)
    keyboard.row(cardano_button)
    bot.send_message(message.chat.id, text, parse_mode='Markdown', disable_web_page_preview=True, reply_markup=keyboard)

@bot.message_handler(commands=['connect'])
def handle_connect(message):
    user = database.get_user(message.chat.id)

    keyboard = types.InlineKeyboardMarkup()
    link_button = types.InlineKeyboardButton('Link Wallet', callback_data='link')
    generate_button = types.InlineKeyboardButton('Generate Wallet', callback_data='generate')
    keyboard.add(link_button)
    keyboard.add(generate_button)

    bot.send_message(message.chat.id, json.dumps(user.wallets, indent=4), reply_markup=keyboard)

@bot.message_handler(commands=['link'])
def handle_link(message):
    bot.send_message(message.chat.id, 'Please enter your wallet details:')
    process_inputs(message.chat.id, input_wallet, input_wallet)

@bot.message_handler(commands=['generate'])
def handle_generate(message):
    handle_link(message)

@bot.message_handler(commands=['sniper'])
def handle_sniper(message):
    user = database.get_user(message.chat.id)

    keyboard = types.InlineKeyboardMarkup()
    configure_button = types.InlineKeyboardButton('Configure', callback_data='configure')
    activate_button = types.InlineKeyboardButton('Activate', callback_data='activate')
    cancel_button = types.InlineKeyboardButton('Cancel', callback_data='cancel')
    keyboard.add(configure_button)
    keyboard.add(activate_button)
    keyboard.add(cancel_button)

    bot.send_message(message.chat.id, json.dumps({**user.configuration, 'active': user.active}, indent=4), reply_markup=keyboard)

@bot.message_handler(commands=['configure'])
def handle_configure(message):
    bot.send_message(message.chat.id, 'Please enter your configuration details:')
    process_inputs(message.chat.id, input_configuration, input_configuration)

@bot.message_handler(commands=['activate'])
def handle_activate(message):
    database.update_user(message.chat.id, 'active', True)
    thread_flags[message.chat.id] = True
    user = database.get_user(message.chat.id)
    thread = threading.Thread(target=sniper.start, args=(message.chat.id, thread_flags, user.wallets, user.configuration, ))
    thread.start()
    bot.send_message(message.chat.id, 'Bot is running')

@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    database.update_user(message.chat.id, 'active', False)
    thread_flags[message.chat.id] = False
    bot.send_message(message.chat.id, 'Bot is stopped')

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
    print('Start Telegram Bot')
    bot.polling()