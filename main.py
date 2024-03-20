import telebot
from telebot import types
import json

import config

configure_properties = {
    'max_gas_price': None,
    'max_gas_limit': None,
    'slippage': None
}

buy_properties = {
    'buy_price': None,
    'buy_quantity': None,
    'min_market_cap': None,
    'max_market_cap': None,
    'min_liquidity': None,
    'max_liquidity': None,
    'max_buy_tax': None,
    'gas_delta': None
}

sell_properties = {
    'target_price_(%)': None,
    'sell_quantity_at_target_(%)': None,
    'stop_loss_(%)': None,
    'sell_quantity_at_stop_loss_(%)': None,
    'max_sell_tax': None,
    'gas_delta': None
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
    bot.send_message(message.chat.id, 'Please enter your configuration details:')
    process_inputs(message.chat.id, configure_properties, configure_properties)

@bot.message_handler(commands=['buy'])
def handle_buy(message):
    bot.send_message(message.chat.id, 'Please enter your auto-buy details:')
    process_inputs(message.chat.id, buy_properties, buy_properties)

@bot.message_handler(commands=['sell'])
def handle_sell(message):
    bot.send_message(message.chat.id, 'Please enter your auto-sell details:')
    process_inputs(message.chat.id, sell_properties, sell_properties)

def process_inputs(chat_id, properties, target):
    property_keys = list(properties.keys())
    if len(property_keys) > 0:
        current_property = property_keys[0]
        bot.send_message(chat_id, f'Enter {current_property.replace('_', ' ')}:')
        bot.register_next_step_handler_by_chat_id(chat_id, lambda message: process_input(chat_id, message, current_property, properties, target))
    else:
        bot.send_message(chat_id, 'Saved successfully.')
        bot.send_message(chat_id, json.dumps(target))

def process_input(chat_id, message, property_key, properties, target):
    try:
        target[property_key] = message.text
        remaining_properties = {key: value for key, value in properties.items() if key != property_key}
        process_inputs(chat_id, remaining_properties, target)
    except Exception as e:
        bot.send_message(chat_id, f'Error: {str(e)}')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'link':
        bot.send_message(call.message.chat.id, 'You selected Link Wallet')
    elif call.data == 'generate':
        bot.send_message(call.message.chat.id, 'You selected Generate Wallet')

bot.polling()
