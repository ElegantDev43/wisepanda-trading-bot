from telebot import types

from src.database import user as user_model
from src.engine import api as main_api
import threading

chain_buy_amounts = [1]
chain_gas_amounts = [0.1, 0.2, 0.3]
chain_gas_prices = [0.1, 0.2, 0.3]
chain_slippages = [50]
chain_limit_token_prices = [171, 173, 175]
chain_market_caps = [10000, 200000, 50000]
chain_liquidities = [10000, 200000, 50000]
chain_taxes = [5, 10, 20]
chain_intervals = [60]
chain_durations = [3]

order_list = [
    {"name": "Market Order", "active": True},
    {"name": "Limit Order", "active": False},
    {"name": "DCA Order", "active": False}
]
x_value_list = {"buy-amount": 0, "gas-amount": 0, "gas-price": 0, "limit-token-price": 0,"stop-loss":0,
                "slippage": 0, "market-capital": 0,  "interval": 0, "duration": 0,'more_btn_index':1}

index_list = {'wallet': 100, 'buy_amount': 100,
              'gas_price': 100, 'gas_amount': 100, 'slippage': 100, 'limit_token_price': 100, 'liquidity': 100,
              'tax': 100, 'market_cap': 100, 'interval': 100, 'duration': 100, 'max_dca_price': 100,
              'min_dca_price': 100, 'order_index': 0, 'stop-loss': 100}

result = {'wallet': 0, 'buy_amount': 0,
          'gas_price': 0, 'gas_amount': 0, 'slippage': 0, 'type': 0, 'token':'',
          'limit_token_price': 0, 'liquidity': 0, 'tax': 0, 'market_cap': 0,
          'interval': 0, 'duration': 0, 'max_dca_price': 0,
          'min_dca_price': 0, 'stop-loss': 0}


def format_number(num):
    if num >= 1_000_000_000:
        formatted_num = f"{num / 1_000_000_000:.3f}B"
    elif num >= 1_000_000:
        formatted_num = f"{num / 1_000_000:.3f}M"
    elif num >= 1_000:
        formatted_num = f"{num / 1_000:.3f}K"
    else:
        formatted_num = f"{num:.18f}"
    return formatted_num


def initialize_x_value():
    x_value_list['buy-amount'] = 0
    x_value_list['gas-amount'] = 0
    x_value_list['gas-price'] = 0
    x_value_list['limit-token-price'] = 0
    x_value_list['slippage'] = 0
    x_value_list['market-capital'] = 0
    x_value_list['liquidity'] = 0
    x_value_list['limit-tax'] = 0


def handle_buyer(bot, message):
   # user_model.create_user_by_telegram(message.chat.id)
    text = '''
🛒 * Token Buy*

Enter a token address to buy.
    '''
    x_value_list['more_btn_index'] = 1
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_token(bot, next_message))


def get_keyboard(order_name, update_data, chat_id, index_data):
   # wallet_count = 4
    # buy_count = 4
    # gas_amount_count = 3

    keyboard = types.InlineKeyboardMarkup()

    if (order_name == "Market Order"):
        market_order = types.InlineKeyboardButton(
            '✅ Market', callback_data='buy-market-orders')
        limit_order = types.InlineKeyboardButton(
            'Limit', callback_data='buy-limit-orders')
        dca_order = types.InlineKeyboardButton(
            'DCA', callback_data='buy-dca-orders')
        for index in order_list:
            index['active'] = False
        order_list[0]['active'] = True
    elif order_name == "Limit Order":
        market_order = types.InlineKeyboardButton(
            'Market', callback_data='buy-market-orders')
        limit_order = types.InlineKeyboardButton(
            '✅ Limit', callback_data='buy-limit-orders')
        dca_order = types.InlineKeyboardButton(
            'DCA', callback_data='buy-dca-orders')
        for index in order_list:
            index['active'] = False
        order_list[1]['active'] = True
    elif order_name == "DCA Order":
        market_order = types.InlineKeyboardButton(
            'Market', callback_data='buy-market-orders')
        limit_order = types.InlineKeyboardButton(
            'Limit', callback_data='buy-limit-orders')
        dca_order = types.InlineKeyboardButton(
            '✅ DCA', callback_data='buy-dca-orders')
        for index in order_list:
            index['active'] = False
        order_list[2]['active'] = True
    keyboard.row(market_order, limit_order, dca_order)

    wallets = []
    more_wallet_btn = types.InlineKeyboardButton('🔽', callback_data='buyer show more wallets')
    chain_wallets = main_api.get_wallets(chat_id)
    wallet_count = len(chain_wallets)
    for index in range(wallet_count):
        caption = f'{"🟢" if index == index_data['wallet'] else ""} W{
            index + 1}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select buy wallet {index}")
        wallets.append(button)
    wallet_all = types.InlineKeyboardButton(
        'All', callback_data=f'select buy wallet all')

    anti_mev = types.InlineKeyboardButton(
        '🔴 Anti-Mev', callback_data=f'anti mev')
    anti_rug = types.InlineKeyboardButton(
        '🔴 Anti-Rug', callback_data=f'anti Rug')

    buys = []
    buy_count = len(chain_buy_amounts)
    amount_title = types.InlineKeyboardButton(
        'Amount:', callback_data='set title')
    for index in range(buy_count):
        if index_data['buy_amount'] == 100:
            caption = f'{chain_buy_amounts[index]} SOL'
        else:
            caption = f'{"🟢" if index == index_data['buy_amount'] else ""} {
                chain_buy_amounts[index]} SOL'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select buy amount {index}")
        buys.append(button)

    if update_data['buy-amount'] == 0:
        caption = "X SOL"
    else:
        caption = f"🟢 {update_data['buy-amount']} SOL"
    buy_x = types.InlineKeyboardButton(
        text=caption, callback_data='select buy amount x')

    slippage_title = types.InlineKeyboardButton(
        'Slippage:', callback_data='set title')
    slippages = []
    slip_page_count = len(chain_slippages)
    for index in range(slip_page_count):
        if index_data['slippage'] == 100:
            caption = f'Auto Slippage'
        else:
            caption = f'{"🟢" if index == index_data['slippage'] else ""} Auto Slippage'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select slippage {index}")
        slippages.append(button)
    if update_data['slippage'] == 0:
        caption = "X% Slippage"
    else:
        caption = f"🟢 {update_data['slippage']}% Slippage"
    slippage_x = types.InlineKeyboardButton(
        text=caption, callback_data='select slippage x')

    market_capital_title = types.InlineKeyboardButton(
        'Max Market Capital:', callback_data='set title')
    if update_data['market-capital'] == 0:
        caption = "X"
    else:
        caption = f"{update_data['market-capital']}"
    market_capital_x = types.InlineKeyboardButton(
        text=caption, callback_data='select market capital x')

    intervals = []
    interval_count = len(chain_intervals)
    for index in range(interval_count):
        if index_data['interval'] == 100:
            caption = f'{chain_intervals[index]}'
        else:
            caption = f'{" 🟢" if index == index_data['interval'] else ""} {
                chain_intervals[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select interval {index}")
        intervals.append(button)
    interval_title = types.InlineKeyboardButton(
        'Interval:', callback_data='set title')
    if update_data['interval'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['interval']}"
    interval_x = types.InlineKeyboardButton(
        text=caption, callback_data='select interval x')

    durations = []
    duration_count = len(chain_durations)
    for index in range(duration_count):
        if index_data['duration'] == 100:
            caption = f'{chain_durations[index]}'
        else:
            caption = f'{" 🟢" if index == index_data['duration'] else ""} {
                chain_durations[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select duration {index}")
        durations.append(button)
    duration_title = types.InlineKeyboardButton(
        'Count:', callback_data='set title')
    if update_data['duration'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['duration']}"
    duration_x = types.InlineKeyboardButton(
        text=caption, callback_data='select duration x')

    create_order = types.InlineKeyboardButton(
        '✔️ Buy', callback_data='make buy order')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')

    if update_data['more_btn_index'] == 1:
      keyboard.row(*wallets[4*(update_data['more_btn_index']-1): 4*(update_data['more_btn_index']-1) + 3], more_wallet_btn)
    else:
      for index in range(update_data['more_btn_index'] - 1):
        keyboard.row(*wallets[4*index: 4 * index + 4])
      last_index = update_data['more_btn_index'] -1
      if 4 * (last_index + 1) <= wallet_count:
        keyboard.row(*wallets[4 * last_index: 4 * last_index + 3], more_wallet_btn)
      else:
        keyboard.row(*wallets[4 * last_index: wallet_count])
        

    keyboard.row(amount_title, *buys[0:buy_count],buy_x)

    current_chain_index = main_api.get_chain(chat_id)
    chains = main_api.get_chains()
    current_chain = chains[current_chain_index]
    keyboard.row(slippage_title, *
                     slippages[0:(len(slippages))], slippage_x)
    if order_name == "Market Order":
      keyboard.row(anti_mev, anti_rug)
    elif order_name == "Limit Order":
        keyboard.row(market_capital_title, market_capital_x)
      #  keyboard.row(market_capital_title)
      #  keyboard.row(
     #       *market_capitals[0:(len(market_capitals))], market_capital_x)
      #  keyboard.row(liquidity_title)
      #  keyboard.row(
      #      *liquidities[0:(len(liquidities))], liquidity_x)
    elif order_name == "DCA Order":
        keyboard.row(interval_title, *intervals[0:(len(intervals))], interval_x)
        keyboard.row(duration_title, *durations[0:(len(durations))], duration_x)

    #keyboard.row(stop_loss_title, stop_loss_x)
    keyboard.row(create_order)
    keyboard.row(back, close)

    return keyboard

def handle_more_btn(bot, message):
    x_value_list['more_btn_index'] += 1
    order_index = ''
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
    
def handle_input_token(bot, message):
    result['token'] = message.text
    
    chain_index = main_api.get_chain(message.chat.id)
    chains = main_api.get_chains()
    current_chain = chains[chain_index]
    token = result['token']
    token_data = main_api.get_token_market_data(message.chat.id, token)
    meta_data = main_api.get_token_metadata(message.chat.id, token)
    
    token_price = format_number(token_data['price'])
    token_liquidity = format_number(token_data['liquidity'])
    token_market_cap = format_number(token_data['market_capital'])
    text = f'''
    *🛒 Token Buy*

Buy your tokens here.

*{meta_data['name']}  (🔗{current_chain})  *
{token}
    
💲 *Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
'''
    order_index = order_list[0]['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def select_buy_wallet(bot, message, index):
    index_list['wallet'] = int(index)
    result['wallet'] = int(index)
    order_index = ''
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def select_buy_amount(bot, message, index):
    index_list['buy_amount'] = int(index)
    result['buy_amount'] = chain_buy_amounts[int(index)]
    x_value_list['buy-amount'] = 0
    order_index = ''
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def select_gas_amount(bot, message, index):
    index_list['gas_amount'] = int(index)
    result['gas_amount'] = chain_gas_amounts[int(index)]
    x_value_list['gas-amount'] = 0
    order_index = ''
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def select_slip_page(bot, message, index):

    index_list['slippage'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['slippage'] = chain_slippages[int(index)]
    x_value_list['slippage'] = 0
    
    chain_index = main_api.get_chain(message.chat.id)
    chains = main_api.get_chains()
    current_chain = chains[chain_index]
    token = result['token']
    token_data = main_api.get_token_market_data(message.chat.id, token)
    meta_data = main_api.get_token_metadata(message.chat.id, token)
      
    token_price = format_number(token_data['price'])
    token_liquidity = format_number(token_data['liquidity'])
    token_market_cap = format_number(token_data['market_capital'])
    text = f'''
      *🛒 Token Buy*

  Buy your tokens here.

  *{meta_data['name']}  (🔗{current_chain})  *
  {token}
      
  💲 *Price:* {token_price}$
  💧 *Liquidity:* {token_liquidity}$
  📊 *Market Cap:* {token_market_cap}$

  [Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
  '''
    order_index = ''
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    

def select_limit_token_price(bot, message, index):
    index_list['limit_token_price'] = int(index)
    result['limit_token_price'] = chain_limit_token_prices[int(index)]
    x_value_list['limit-token-price'] = 0
    order_index = ''
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def select_limit_tax(bot, message, index):
    x_value_list['limit-tax'] = 0
    index_list['tax'] = int(index)
    result['tax'] = chain_taxes[int(index)]
    order_index = ''
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def select_market_capital(bot, message, index):
    x_value_list['market-capital'] = 0
    index_list['market_cap'] = int(index)
    result['market_cap'] = chain_market_caps[int(index)]
    order_index = ''
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def select_liquidity(bot, message, index):
    x_value_list['liquidity'] = 0
    index_list['liquidity'] = int(index)
    result['liquidity'] = chain_liquidities[int(index)]
    order_index = ''
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def select_interval(bot, message, index):
    x_value_list['interval'] = 0
    index_list['interval'] = int(index)
    result['interval'] = chain_intervals[int(index)]
    order_index = ''
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def select_duration(bot, message, index):
    x_value_list['duration'] = 0
    index_list['duration'] = int(index)
    result['duration'] = chain_durations[int(index)]
    order_index = ''
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_select_auto_slippage(bot, message, index):
  text = '''
      *🛒 Token Buy*
 Do you confirm 50% slippage as Auto Slippage?.
'''
  keyboard = types.InlineKeyboardMarkup()
  cancel = types.InlineKeyboardButton('Cancel', callback_data='select slippage x')
  confirm = types.InlineKeyboardButton('Confirm', callback_data=f'confirm select slippage {index}')
  keyboard.row(cancel, confirm)
  bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                    reply_markup=keyboard, disable_web_page_preview=True)
  
def handle_buy_amount_x(bot, message):
    text = '''
*Token Buy > 💰 X*
Enter the amount to buy:
'''
    item = "Buy Amount"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_gas_amount_x(bot, message):
    text = '''
*Token Buy > ⛽ X*
Enter the gas amount to set:
'''
    item = "Gas Amount"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_slippage_x(bot, message):
    text = '''
*Token Buy > 💧 X%*
Enter the slippage to set:
'''
    item = "Slippage"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_stop_loss_x(bot, message):
    text = '''
*Token Buy > 💧 X%*
Enter the slippage to set:
'''
    item = "Stop Loss"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))
 
def handle_limit_token_price_x(bot, message):
    text = '''
*Token Buy > 💰 X*
Enter the Token Price to set:
'''
    item = "Token Price"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_market_capital_x(bot, message):
    text = '''
*Token Buy > 💰 X*
Enter the Maximum Market Capital to set:
'''
    item = "Market Capital"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_liquidity_x(bot, message):
    text = '''
*Token Buy > 💰 X*
Enter the liquidity to set:
'''
    item = "Liquidity"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_limit_tax_x(bot, message):
    text = '''
*Token Buy > 💰 X%*
Enter the tax to set:
'''
    item = "Tax"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_duration_x(bot, message):
    text = '''
*Token Buy > 🕞 X*
Enter the duration to set:
'''
    item = "Duration"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_interval_x(bot, message):
    text = '''
*Token Buy > 🕞 X*
Enter the interval to set:
'''
    item = "Interval"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_max_price_x(bot, message):
    text = '''
*Token Buy > 💰 X*
Enter the max price to set:
'''
    item = "Max Price"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_min_price_x(bot, message):
    text = '''
*Token Buy > 💰 X*
Enter the min price to set:
'''
    item = "Min Price"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_input_value(bot, message, item):
    if item == "Buy Amount":
        buy_amount_x = float(message.text)
        x_value_list['buy-amount'] = buy_amount_x
        result['buy_amount'] = buy_amount_x
        index_list['buy_amount'] = 100
    elif item == "Gas Amount":
        gas_amount_x = float(message.text)
        x_value_list['gas-amount'] = gas_amount_x
        result['gas_amount'] = gas_amount_x
        index_list['gas_amount'] = 100
    elif item == "Gas Price":
        gas_price_x = float(message.text)
        x_value_list['gas-price'] = gas_price_x
        result['gas_price'] = gas_price_x
        index_list['gas_price'] = 100
    elif item == "Slippage":
        slippage_x = float(message.text)
        x_value_list['slippage'] = slippage_x
        result['slippage'] = slippage_x
        index_list['slippage'] = 100
    elif item == "Token Price":
        token_price_x = float(message.text)
        x_value_list['limit-token-price'] = token_price_x
        result['limit_token_price'] = token_price_x
        index_list['limit_token_price'] = 100
    elif item == "Stop Loss":
        token_price_x = float(message.text)
        x_value_list['stop-loss'] = token_price_x
        result['stop-loss'] = token_price_x
        index_list['stop-loss'] = 100
    elif item == "Market Capital":
        market_capital_x = float(message.text)
        x_value_list['market-capital'] = market_capital_x
        result['market_cap'] = market_capital_x
        index_list['market_cap'] = 100
    elif item == "Liquidity":
        slippage_x = float(message.text)
        x_value_list['liquidity'] = slippage_x
        result['liquidity'] = slippage_x
        index_list['liquidity'] = 100
    elif item == "Tax":
        slippage_x = float(message.text)
        x_value_list['limit-tax'] = slippage_x
        result['tax'] = slippage_x
        index_list['tax'] = 100
    elif item == "Interval":
        slippage_x = float(message.text)
        x_value_list['interval'] = slippage_x
        result['interval'] = slippage_x
        index_list['interval'] = 100
    elif item == "Duration":
        slippage_x = float(message.text)
        x_value_list['duration'] = slippage_x
        result['duration'] = slippage_x
        index_list['duration'] = 100
    elif item == "Max Price":
        slippage_x = float(message.text)
        x_value_list['dca-max-price'] = slippage_x
        result['max_dca_price'] = slippage_x
        index_list['max_dca_price'] = 100
    elif item == "Min Price":
        slippage_x = float(message.text)
        x_value_list['dca-min-price'] = slippage_x
        result['min_dca_price'] = slippage_x
        index_list['min_dca_price'] = 100
    order_index = ''
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)
    
    chain_index = main_api.get_chain(message.chat.id)
    chains = main_api.get_chains()
    current_chain = chains[chain_index]
    token = result['token']
    token_data = main_api.get_token_market_data(message.chat.id, token)
    meta_data = main_api.get_token_metadata(message.chat.id, token)
    
    token_price = format_number(token_data['price'])
    token_liquidity = format_number(token_data['liquidity'])
    token_market_cap = format_number(token_data['market_capital'])
    text = f'''
    *🛒 Token Buy*

Buy your tokens here.

*{meta_data['name']}  (🔗{current_chain})  *
{token}
    
💲 *Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def handle_buy(bot, message):
    result['type'] = 0
    order_name = ""
    for index in order_list:
        if index['active'] == True:
            order_name = index['name']

    chain_index = main_api.get_chain(message.chat.id)
    chains = main_api.get_chains()
    wallets = main_api.get_wallets(message.chat.id)
    buy_wallet = wallets[result['wallet']]['id']
    buy_amount = int(result['buy_amount'] * 1_000_000_000)
    print(result['token'])
    
    if order_name == "Market Order":
        bot.send_message(chat_id=message.chat.id,
                     text='Buy Transaction sent. Please take for about 10 seconds to be confirmed')
        position = main_api.market_buy(message.chat.id, result['token'], buy_amount, result['slippage'], buy_wallet, False)
        result_text = f'''Successfully confirmed Buy Transaction.
Transaction ID: {position['transaction_id']}
View on SolScan: (https://solscan.io/tx/{position['transaction_id']})'''
        bot.send_message(chat_id=message.chat.id,
                     text=result_text)
    elif order_name == "Limit Order":
        main_api.add_limit_buy(message.chat.id, result['token'], buy_amount, int(result['slippage']), buy_wallet, float(result['market_cap']))
        bot.send_message(chat_id=message.chat.id,
                     text='Successfully registered Order.')
    elif order_name == "DCA Order":
        main_api.add_dca_buy(message.chat.id,result['token'], buy_amount, result['slippage'], buy_wallet,  result['interval'], result['duration'])
        bot.send_message(chat_id=message.chat.id,
                     text='Successfully registered Order.')

def handle_limit_order(bot, message):
    order_index = "Limit Order"
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_market_order(bot, message):
    order_index = "Market Order"
    index_list['order_index'] = 1
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_dca_order(bot, message):
    order_index = "DCA Order"
    index_list['order_index'] = 2
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
