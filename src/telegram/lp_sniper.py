from telebot import types

from src.database import user as user_model
from src.engine import api as main_api
import threading
chain_buy_amounts = [0.01, 0.03, 0.05, 0.1]
chain_gas_prices = [0.1, 0.2, 0.3]
chain_slippages = [5, 10, 20]
chain_limit_token_prices = [500, 1000, 2000]

chain_auto_sell_params = [{'amount': 100, 'price': 0}, {'amount': 50, 'price': 0}]
x_value_list = {"buy-amount": 0, "token_price": 0, 'slippage': 0, "liquidity":0,"market_cap":0, "tk_count":0,"auto_amount":0, "auto_price":0}

index_list = {'wallet': 100}

result = {'wallet': 0, 'token': '', 'buy_amount': 0, 'slippage': 0,
          'limit_token_price': 0, 'stop-loss':0}

auto_sell_status = {'index':0}

def initialize_x_value():
    x_value_list['buy-amount'] = 0
    x_value_list['gas-amount'] = 0
    x_value_list['gas-price'] = 0
    x_value_list['limit-token-price'] = 0
    x_value_list['slippage'] = 0


def get_keyboard(update_data, chat_id, index_data):
   # wallet_count = 4
    # buy_count = 4
    # gas_amount_count = 3

    keyboard = types.InlineKeyboardMarkup()

    wallets = []

    chain_wallets = main_api.get_wallets(chat_id)
    wallet_count = len(chain_wallets)
    for index in range(wallet_count):
        caption = f'{"🟢" if index == index_data['wallet'] else ""} W{
            index + 1}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"lp sniper select buy wallet {index}")
        wallets.append(button)
        
    amount_title = types.InlineKeyboardButton(
        'Amount:', callback_data='set title')
    if update_data['buy-amount'] == 0:
        caption = "💰 XΞ"
    else:
        caption = f"💰 {update_data['buy-amount']}Ξ"
    buy_x = types.InlineKeyboardButton(
        text=caption, callback_data='lp_sniper_input buy-amount')

    slippage_title = types.InlineKeyboardButton(
        'Slippage:', callback_data='set title')
    if update_data['slippage'] == 0:
        caption = "X %"
    else:
        caption = f"{update_data['slippage']}%"
    slippage_x = types.InlineKeyboardButton(
        text=caption, callback_data='lp_sniper_input slippage')
    
    tk_count_title = types.InlineKeyboardButton(
        'Count:', callback_data='set title')
    if update_data['tk_count'] == 0:
        caption = "X"
    else:
        caption = f"{update_data['tk_count']}"
    tk_count_x = types.InlineKeyboardButton(
        text=caption, callback_data='lp_sniper_input tk_count')
# limit order
    limit_token_price_title = types.InlineKeyboardButton(
        'Criteria:', callback_data='set title')
    if update_data['token_price'] == 0:
        caption = "X"
    else:
        caption = f"{update_data['token_price']}"
    limit_token_price_x = types.InlineKeyboardButton(
        text=caption, callback_data='lp_sniper_input token_price')
    
    liquidity_title = types.InlineKeyboardButton(
        'Liquidity:', callback_data='set title')
    if update_data['liquidity'] == 0:
        caption = "X"
    else:
        caption = f"{update_data['liquidity']}"
    liquidity_x = types.InlineKeyboardButton(
        text=caption, callback_data='lp_sniper_input liquidity')

    market_cap_title = types.InlineKeyboardButton(
        'MCap:', callback_data='set title')
    if update_data['market_cap'] == 0:
        caption = "X"
    else:
        caption = f"{update_data['market_cap']}"
    market_cap_x = types.InlineKeyboardButton(
        text=caption, callback_data='lp_sniper_input market_cap')
    
    auto_sell = types.InlineKeyboardButton(
        '🔻 Auto Sell', callback_data='lp sniper set auto_sell')
    
    auto_amount_title = types.InlineKeyboardButton(
        'Amount:', callback_data='2')
    auto_price_title = types.InlineKeyboardButton(
        'Price:', callback_data='2')
    auto_add_button = types.InlineKeyboardButton(
        'Add', callback_data='lp sniper add auto params')


    auto_amounts = []
    for index in range(len(chain_auto_sell_params)):
      auto_amount_x = types.InlineKeyboardButton(
          text=f'''{chain_auto_sell_params[index]['amount']}''', callback_data=f'lp sniper select auto amount {index}')
      auto_amounts.append(auto_amount_x)
    
    auto_prices = []
    for index in range(len(chain_auto_sell_params)):
      auto_price_x = types.InlineKeyboardButton(
          text=f'''{chain_auto_sell_params[index]['price']}''', callback_data=f'lp sniper select auto price {index}')
      auto_prices.append(auto_price_x)

    auto_removes = []
    for index in range(len(chain_auto_sell_params)):
      auto_remove_x = types.InlineKeyboardButton(
          text='remove', callback_data=f'lp sniper remove auto params {index}')
      auto_removes.append(auto_remove_x)
      
    create_order = types.InlineKeyboardButton(
        '✔️ Set Sniper', callback_data='make sniper order')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')

    keyboard.row(amount_title, buy_x, slippage_title, slippage_x)
    keyboard.row(*wallets[0:(wallet_count)])
    keyboard.row(tk_count_title, tk_count_x)
    keyboard.row(limit_token_price_title, limit_token_price_x, liquidity_title, liquidity_x, market_cap_title, market_cap_x)
    keyboard.row(auto_sell)
    if auto_sell_status['index'] == 1:
      for index in range(len(chain_auto_sell_params)):
        keyboard.row(auto_amount_title, auto_amounts[index], auto_price_title, auto_prices[index], auto_removes[index])
      keyboard.row(auto_add_button)
    keyboard.row(create_order)
    keyboard.row(back, close)

    return keyboard


def handle_lp_sniper(bot, message):
   # user = user_model.get_user_by_telegram(message.chat.id)
    token = result['token']
    chain = 'ethereum'

    name = "elo"

    text = f'''
    *LP Sniper*
    Introducing our LP Sniper function: a powerful tool designed
    to automatically and accurately snipe liquidity pools,
    providing you with the best entry points to maximize your
    trading efficiency and returns.
    '''
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def handle_auto_sell(bot, message):
    text = f'''
    *LP Sniper*
    Introducing our LP Sniper function: a powerful tool designed
    to automatically and accurately snipe liquidity pools,
    providing you with the best entry points to maximize your
    trading efficiency and returns.
    '''
    auto_sell_status['index'] = 1
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def select_buy_wallet(bot, message, index):
   # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]'
    index_list['wallet'] = int(index)
    result['wallet'] = int(index)

    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def handle_input_x(bot, message, item):
    text = '''
*LP Sniper > X*
Enter the value to set:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_input_value(bot, message, item):
    x_value_list[item] = message.text
    result[item] = message.text

    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    text = f'''
    *LP Sniper*
    Introducing our LP Sniper function: a powerful tool designed
    to automatically and accurately snipe liquidity pools,
    providing you with the best entry points to maximize your
    trading efficiency and returns.
    '''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)



def handle_auto_amount_value(bot, message,index):
    text = '''
*Token Sniper > 💰 X*
Enter the Amount to set:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_auto_amount_input_value(bot, next_message, index))

def handle_auto_price_value(bot, message,index):
    text = '''
*Token Sniper > 💰 X*
Enter the Price to set:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_auto_price_input_value(bot, next_message, index))


def handle_auto_amount_input_value(bot, message, index):
    item = int(index)
    chain_auto_sell_params[item]['amount'] = message.text
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    text = f'''
    *LP Sniper*
    Introducing our LP Sniper function: a powerful tool designed
    to automatically and accurately snipe liquidity pools,
    providing you with the best entry points to maximize your trading efficiency and returns.
    '''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def handle_auto_price_input_value(bot, message, index):
    item = int(index)
    chain_auto_sell_params[item]['price'] = message.text
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    text = f'''
    *LP Sniper*
    Introducing our LP Sniper function: a powerful tool designed
    to automatically and accurately snipe liquidity pools,
    providing you with the best entry points to maximize your trading efficiency and returns.
    '''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def handle_remove_auto_params(bot, message, index):
    item = int(index)
    chain_auto_sell_params.pop(item)
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    text = f'''
    *LP Sniper*
    Introducing our LP Sniper function: a powerful tool designed
    to automatically and accurately snipe liquidity pools,
    providing you with the best entry points to maximize your trading efficiency and returns.
    '''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def add_auto_param(bot, message):
    new_param = {'amount':0, 'price':0}
    chain_auto_sell_params.append(new_param)
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    text = f'''
    *LP Sniper*
    Introducing our LP Sniper function: a powerful tool designed
    to automatically and accurately snipe liquidity pools,
    providing you with the best entry points to maximize your trading efficiency and returns.
    '''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def handle_set_sniper(bot, message):
    chain_index = main_api.get_chain(message.chat.id)
    main_api.add_token_sniper(message.chat.id, result['token'], result['buy_amount'], result['slippage'], result['wallet'], result['limit_token_price'], result['stop-loss'], chain_auto_sell_params)
    bot.send_message(chat_id=message.chat.id,
                     text='Successfully registered Sniper')
