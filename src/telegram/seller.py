from telebot import types

from src.database import user as user_model
from src.engine import api as main_api
import threading

chain_buy_amounts = [50]
chain_slippages = [10]
chain_limit_token_prices = [500, 1000, 2000]
chain_market_caps = [10000, 200000, 50000]
chain_liquidities = [10000, 200000, 50000]
chain_taxes = [5, 10, 20]
chain_intervals = [10, 20, 30]
chain_durations = [3, 6]
chain_dca_max_prices = [10000, 20000, 30000]
chain_dca_min_prices = [1000, 2000, 3000]
chain_stop_losses = [5, 10, 20]

order_list = [
    {"name": "Market Order", "active": True},
    {"name": "Limit Order", "active": False},
    {"name": "DCA Order", "active": False}
]
x_value_list = {"buy-amount": 0, "gas-amount": 0, "gas-price": 0, "limit-token-price": 0,
                "slippage": 0, "market-capital": 0, "liquidity": 0, "limit-tax": 0, "stop-loss": 0, "interval": 0,
                "duration": 0, "dca-max-price": 0, "dca-min-price": 0}

index_list = {'position': 100, 'buy_amount': 100,
              'gas_price': 100, 'gas_amount': 100, 'slippage': 100, 'limit_token_price': 100, 'liquidity': 100,
              'tax': 100, 'market_cap': 100, 'stop-loss': 0, 'interval': 100, 'duration': 100, 'max_dca_price': 100,
              'min_dca_price': 100, 'order_index': 0}

result = {'position': 0, 'buy_amount': 0,
          'gas_price': 0, 'gas_amount': 0, 'slippage': 0, 'type': 0, 'token': "",
          'limit_token_price': 0, 'liquidity': 0, 'tax': 0, 'market_cap': 0, 'stop-loss': 0,
          'interval': 0, 'duration': 0, 'max_dca_price': 0,
          'min_dca_price': 0}

def format_number(num):
    if num >= 1_000_000_000:
        formatted_num = f"{num / 1_000_000_000:.3f}B"
    elif num >= 1_000_000:
        formatted_num = f"{num / 1_000_000:.3f}M"
    elif num >= 1_000:
        formatted_num = f"{num / 1_000:.3f}K"
    else:
        formatted_num = f"{num:.3f}"
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


def handle_positions(bot, message):
    chain_positions = main_api.get_positions(message.chat.id)
    text = f'''
            *🛒 Token Sell*
            
You currently have {len(chain_positions)} positions.

Select position to sell tokens.
'''
    keyboard = types.InlineKeyboardMarkup()
    positions = []
    chain_positions = main_api.get_positions(message.chat.id)
    position_count = len(chain_positions)
    wallets = main_api.get_wallets(message.chat.id)
    for index in range(position_count):
      for item in range(len(wallets)):
        if wallets[item]['id'] == chain_positions[index]['wallet_id']:
          meta = main_api.get_token_metadata(message.chat.id, chain_positions[index]['token'])
          caption = f'Token: {meta['symbol']}, Amount:{chain_positions[index]['amount']}, W{item}'
      button = types.InlineKeyboardButton(
            text=caption, callback_data=f"seller select position {index}")
      positions.append(button)
    for item in positions:
      keyboard.row(item)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def get_keyboard(order_name, update_data, chat_id, index_data):
   # wallet_count = 4
    # buy_count = 4
    # gas_amount_count = 3

    keyboard = types.InlineKeyboardMarkup()

    if (order_name == "Market Order"):
        market_order = types.InlineKeyboardButton(
            '✅ Market', callback_data='seller-market-orders')
        limit_order = types.InlineKeyboardButton(
            'Limit', callback_data='seller-limit-orders')
        dca_order = types.InlineKeyboardButton(
            'DCA', callback_data='seller-dca-orders')
        for index in order_list:
            index['active'] = False
        order_list[0]['active'] = True
    elif order_name == "Limit Order":
        market_order = types.InlineKeyboardButton(
            'Market', callback_data='seller-market-orders')
        limit_order = types.InlineKeyboardButton(
            '✅ Limit', callback_data='seller-limit-orders')
        dca_order = types.InlineKeyboardButton(
            'DCA', callback_data='seller-dca-orders')
        for index in order_list:
            index['active'] = False
        order_list[1]['active'] = True
    elif order_name == "DCA Order":
        market_order = types.InlineKeyboardButton(
            'Market', callback_data='seller-market-orders')
        limit_order = types.InlineKeyboardButton(
            'Limit', callback_data='seller-limit-orders')
        dca_order = types.InlineKeyboardButton(
            '✅ DCA', callback_data='seller-dca-orders')
        for index in order_list:
            index['active'] = False
        order_list[2]['active'] = True
    keyboard.row(market_order, limit_order, dca_order)

    anti_mev = types.InlineKeyboardButton(
        '🔴 Anti-Mev', callback_data=f'anti mev')
    anti_rug = types.InlineKeyboardButton(
        '🔴 Anti-Rug', callback_data=f'anti Rug')





    buys = []
    buy_count = len(chain_buy_amounts)
    for index in range(buy_count):
        if index_data['buy_amount'] == 100:
            caption = f'💰{chain_buy_amounts[index]}%'
        else:
            caption = f'{"🟢" if index == index_data['buy_amount'] else ""} 💰{
                chain_buy_amounts[index]}%'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"seller select buy amount {index}")
        buys.append(button)

    if update_data['buy-amount'] == 0:
        caption = "💰 X%"
    else:
        caption = f"🟢 💰 {update_data['buy-amount']}%"
    buy_x = types.InlineKeyboardButton(
        text=caption, callback_data='seller select buy amount x')

    slippages = []
    slip_page_count = len(chain_slippages)
    for index in range(slip_page_count):
        if index_data['slippage'] == 100:
            caption = f'{chain_slippages[index]}%'
        else:
            caption = f'{" 🟢" if index == index_data['slippage'] else ""} {
                chain_slippages[index]}%'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"seller select slippage {index}")
        slippages.append(button)
    slippage_title = types.InlineKeyboardButton(
        'Slippage:', callback_data='set title')
    if update_data['slippage'] == 0:
        caption = "X %"
    else:
        caption = f"🟢 {update_data['slippage']}%"
    slippage_x = types.InlineKeyboardButton(
        text=caption, callback_data='seller select slippage x')
# limit order

    limit_token_price_title = types.InlineKeyboardButton(
        'Token Price:', callback_data='set title')
    if update_data['limit-token-price'] == 0:
        caption = "X"
    else:
        caption = f"{update_data['limit-token-price']}"
    limit_token_price_x = types.InlineKeyboardButton(
        text=caption, callback_data='seller select limit token price x')
    
    intervals = []
    interval_count = len(chain_intervals)
    for index in range(interval_count):
        if index_data['interval'] == 100:
            caption = f'{chain_intervals[index]}'
        else:
            caption = f'{" 🟢" if index == index_data['interval'] else ""} {
                chain_intervals[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"seller select interval {index}")
        intervals.append(button)
    interval_title = types.InlineKeyboardButton(
        'Interval:', callback_data='set title')
    if update_data['interval'] == 0:
        caption = "X min"
    else:
        caption = f"🟢 {update_data['interval']} min"
    interval_x = types.InlineKeyboardButton(
        text=caption, callback_data='seller select interval x')

   
    duration_title = types.InlineKeyboardButton(
        'Count:', callback_data='set title')
    if update_data['duration'] == 0:
        caption = "X"
    else:
        caption = f"{update_data['duration']}"
    duration_x = types.InlineKeyboardButton(
        text=caption, callback_data='seller select duration x')

    dca_max_price_title = types.InlineKeyboardButton(
        'Max Price:', callback_data='set title')
    if update_data['dca-max-price'] == 0:
        caption = "X"
    else:
        caption = f"{update_data['dca-max-price']}"
    dca_max_price_x = types.InlineKeyboardButton(
        text=caption, callback_data='seller select max price x')

   
    dca_min_price_title = types.InlineKeyboardButton(
        'Min Price:', callback_data='set title')
    if update_data['dca-min-price'] == 0:
        caption = "X"
    else:
        caption = f"{update_data['dca-min-price']}"
    dca_min_price_x = types.InlineKeyboardButton(
        text=caption, callback_data='seller select min price x')

    create_order = types.InlineKeyboardButton(
        '✔️ Sell', callback_data='make sell order')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')

    keyboard.row(*buys[0:(buy_count // 2)])
    keyboard.row(*buys[(buy_count // 2):buy_count], buy_x)
    keyboard.row(slippage_title,*slippages[0:(len(slippages))], slippage_x)
    if order_name == "Market Order":
        keyboard.row(anti_mev, anti_rug)
    elif order_name == "Limit Order":
        keyboard.row(limit_token_price_title, limit_token_price_x)
    elif order_name == "DCA Order":
        keyboard.row(interval_title,
            *intervals[0:(len(intervals))], interval_x)
        keyboard.row(duration_title, duration_x)
        keyboard.row(dca_min_price_title, dca_min_price_x,dca_max_price_title, dca_max_price_x)
    keyboard.row(create_order)
    keyboard.row(back, close)

    return keyboard


def select_buy_amount(bot, message, index):
   # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    index_list['buy_amount'] = int(index)
    result['buy_amount'] = chain_buy_amounts[int(index)]
    x_value_list['buy-amount'] = 0

    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_gas_amount(bot, message, index):
  #  user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    index_list['gas_amount'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    keyboards = main_api.get_keyboards(message.chat.id)
    result['gas_amount'] = keyboards['gas'][int(index)]
    x_value_list['gas-amount'] = 0
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_slip_page(bot, message, index):
   # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    index_list['slippage'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['slippage'] = chain_slippages[int(index)]
    x_value_list['slippage'] = 0
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_stop_loss(bot, message, index):
    # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    index_list['stop-loss'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['stop-loss'] = chain_stop_losses[int(index)]
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    x_value_list['stop-loss'] = 0
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_limit_tax(bot, message, index):
  #  user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    x_value_list['limit-tax'] = 0
    index_list['tax'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['tax'] = chain_taxes[int(index)]
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_market_capital(bot, message, index):
  #  user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    x_value_list['market-capital'] = 0
    index_list['market_cap'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['market_cap'] = chain_market_caps[int(index)]
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_liquidity(bot, message, index):
   # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    x_value_list['liquidity'] = 0
    index_list['liquidity'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['liquidity'] = chain_liquidities[int(index)]
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_interval(bot, message, index):
  #  user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    x_value_list['interval'] = 0
    index_list['interval'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['interval'] = chain_liquidities[int(index)]
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_duration(bot, message, index):
  #  user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    x_value_list['duration'] = 0
    index_list['duration'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['duration'] = chain_liquidities[int(index)]
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_max_price(bot, message, index):
   # chain = user.chain
    #  wallets = user.wallets[chain]
    x_value_list['dca-max-price'] = 0
    index_list['max_dca_price'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['max_dca_price'] = chain_liquidities[int(index)]
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_min_price(bot, message, index):
    # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    x_value_list['dca-min-price'] = 0
    index_list['min_dca_price'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['min_dca_price'] = chain_liquidities[int(index)]
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def handle_buy_amount_x(bot, message):
    text = '''
*Token Sell > 💰 X*
Enter the amount to sell:
'''
    item = "Buy Amount"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_gas_amount_x(bot, message):
    text = '''
*Token Sell > ⛽ X*
Enter the gas amount to set:
'''

    item = "Gas Amount"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_gas_price_x(bot, message):
    text = '''
*Token Sell > ⛽ X*
Enter the gas price to set:
'''
    item = "Gas Price"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_slippage_x(bot, message):
    text = '''
*Token Sell > 💧 X%*
Enter the slippage to set:
'''
    item = "Slippage"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_stop_loss_x(bot, message):
    text = '''
*Token Sell > 💰 X*
Enter the Stop Loss to set:
'''
    item = "Token Price"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_market_capital_x(bot, message):
    text = '''
*Token Sell > 💰 X*
Enter the Maximum Market Capital to set:
'''
    item = "Market Capital"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_liquidity_x(bot, message):
    text = '''
*Token Sell > 💰 X*
Enter the liquidity to set:
'''
    item = "Liquidity"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_limit_tax_x(bot, message):
    text = '''
*Token Sell > 💰 X%*
Enter the tax to set:
'''
    item = "Tax"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_limit_token_price_x(bot, message):
    text = '''
*Token Sell > 💰 X*
Enter the limit price to set:
'''
    item = "Token Price"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))
    
def handle_duration_x(bot, message):
    text = '''
*Token Sell > 🕞 X*
Enter the duration to set:
'''
    item = "Duration"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_interval_x(bot, message):
    text = '''
*Token Sell > 🕞 X*
Enter the interval to set:
'''
    item = "Interval"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_max_price_x(bot, message):
    text = '''
*Token Sell > 💰 X*
Enter the max price to set:
'''
    item = "Max Price"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_min_price_x(bot, message):
    text = '''
*Token Sell > 💰 X*
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
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    chain_index = main_api.get_chain(message.chat.id)
    chains = main_api.get_chains()
    current_chain = chains[chain_index]
    
    chain_positions = main_api.get_positions(message.chat.id)
    index = index_list['position']
    token = chain_positions[index]['token']
    token_data = main_api.get_token_market_data(message.chat.id, token)
    meta_data = main_api.get_token_metadata(message.chat.id, token)
      
    token_price = format_number(token_data['price'])
    token_liquidity = format_number(token_data['liquidity'])
    token_market_cap = format_number(token_data['market_capital'])
    text = f'''
      *🛒 Token Sell*

  Sell your tokens here.

  *{meta_data['name']}  (🔗{current_chain})  *
  {token}
      
  💲 *Price:* {token_price}$
  💧 *Liquidity:* {token_liquidity}$
  📊 *Market Cap:* {token_market_cap}$

  [Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
  '''

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def handle_buy_amount(bot, message, amount):
    order_amount = amount


def handle_sell(bot, message):
    result['type'] = 1
    order_name = ""
    for index in order_list:
        if index['active'] == True:
            order_name = index['name']

    positions = main_api.get_positions(message.chat.id)
    sell_position = positions[result['position']]['id']
    print(sell_position)
    if order_name == "Market Order":
        print(result['buy_amount'], result['slippage'])
        tx_id, amount = main_api.market_sell(message.chat.id, sell_position,result['buy_amount'], result['slippage'])
    elif order_name == "Limit Order":
        main_api.limit_order(message.chat.id, result)
    elif order_name == "DCA Order":
        main_api.dca_order(message.chat.id, result)
    bot.send_message(chat_id=message.chat.id,
                     text='Successfully registered Order')


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

def select_position(bot, message, item):
  index = int(item)
  index_list['position'] = index
  order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
  for order in order_list:
        if order['active'] == True:
            order_index = order['name']
  
  chain_index = main_api.get_chain(message.chat.id)
  chains = main_api.get_chains()
  current_chain = chains[chain_index]
  
  chain_positions = main_api.get_positions(message.chat.id)
  token = chain_positions[index]['token']
  token_data = main_api.get_token_market_data(message.chat.id, token)
  meta_data = main_api.get_token_metadata(message.chat.id, token)
    
  token_price = format_number(token_data['price'])
  token_liquidity = format_number(token_data['liquidity'])
  token_market_cap = format_number(token_data['market_capital'])
  text = f'''
    *🛒 Token Sell*

Sell your tokens here.

*{meta_data['name']}  (🔗{current_chain})  *
{token}
    
💲 *Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
'''

  keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)
  bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)