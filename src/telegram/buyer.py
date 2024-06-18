from telebot import types

from src.database import user as user_model
from src.engine import api as main_api
import threading

chain_buy_amounts = [0.01, 0.03, 0.05, 0.1]
chain_gas_amounts = [0.1, 0.2, 0.3]
chain_gas_prices = [0.1, 0.2, 0.3]
chain_slippages = [0.5, 3, 5]
chain_limit_token_prices = [171, 173, 175]
chain_market_caps = [10000, 200000, 50000]
chain_liquidities = [10000, 200000, 50000]
chain_taxes = [5, 10, 20]
chain_intervals = [1, 2, 3]
chain_durations = [1, 3, 5]
chain_dca_max_prices = [10000, 20000, 30000]
chain_dca_min_prices = [1000, 2000, 3000]

order_list = [
    {"name": "Market Order", "active": True},
    {"name": "Limit Order", "active": False},
    {"name": "DCA Order", "active": False}
]
x_value_list = {"buy-amount": 0, "gas-amount": 0, "gas-price": 0, "limit-token-price": 0,
                "slippage": 0, "market-capital": 0, "liquidity": 0, "limit-tax": 0, "interval": 0, "duration": 0, "dca-max-price": 0, "dca-min-price": 0}

index_list = {'wallet': 100, 'buy_amount': 100,
              'gas_price': 100, 'gas_amount': 100, 'slippage': 100, 'limit_token_price': 100, 'liquidity': 100,
              'tax': 100, 'market_cap': 100, 'interval': 100, 'duration': 100, 'max_dca_price': 100,
              'min_dca_price': 100, 'order_index': 0, 'stop-loss': 0}

result = {'wallet': 0, 'buy_amount': 0,
          'gas_price': 0, 'gas_amount': 0, 'slippage': 0, 'type': 0, 'token':'',
          'limit_token_price': 0, 'liquidity': 0, 'tax': 0, 'market_cap': 0,
          'interval': 0, 'duration': 0, 'max_dca_price': 0,
          'min_dca_price': 0, 'stop-loss': 0}


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
🛒 * Token Sniper*

Enter a token symbol or address to buy.
    '''

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
    for index in range(buy_count):
        if index_data['buy_amount'] == 100:
            caption = f'💰{chain_buy_amounts[index]}Ξ'
        else:
            caption = f'{"🟢" if index == index_data['buy_amount'] else ""} 💰{
                chain_buy_amounts[index]}Ξ'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select buy amount {index}")
        buys.append(button)

    if update_data['buy-amount'] == 0:
        caption = "💰 XΞ"
    else:
        caption = f"🟢 💰 {update_data['buy-amount']}Ξ"
    buy_x = types.InlineKeyboardButton(
        text=caption, callback_data='select buy amount x')

    gas_amount_count = len(chain_gas_amounts)
    gas_amounts = []
    for index in range(gas_amount_count):
        if index_data['gas_amount'] == 100:
            caption = f'{chain_gas_amounts[index]}'
        else:
            caption = f'{" 🟢" if index == index_data['gas_amount'] else ""} {
                chain_gas_amounts[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select gas amount {index}")
        gas_amounts.append(button)
    gas_amount_title = types.InlineKeyboardButton(
        '----- Gas Amount -----', callback_data='set title')

    if update_data['gas-amount'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['gas-amount']}"
    gas_amount_x = types.InlineKeyboardButton(
        text=caption, callback_data='select gas amount x')

    gas_prices = []
    gas_price_count = len(chain_gas_prices)
    for index in range(gas_price_count):
        if index_data['gas_price'] == 100:
            caption = f'{chain_gas_prices[index]}'
        else:
            caption = f'{" 🟢" if index == index_data['gas_price'] else ""} {
                chain_gas_prices[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select gas price {index}")
        gas_prices.append(button)
    gas_price_title = types.InlineKeyboardButton(
        '----- Gas Price -----', callback_data='set title')
    if update_data['gas-price'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['gas-price']}"
    gas_price_x = types.InlineKeyboardButton(
        text=caption, callback_data='select gas price x')

    slippages = []
    slip_page_count = len(chain_slippages)
    for index in range(slip_page_count):
        if index_data['slippage'] == 100:
            caption = f'{chain_slippages[index]}%'
        else:
            caption = f'{" 🟢" if index == index_data['slippage'] else ""} {
                chain_slippages[index]}%'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select slippage {index}")
        slippages.append(button)
    slippage_title = types.InlineKeyboardButton(
        'Slippage:', callback_data='set title')
    if update_data['slippage'] == 0:
        caption = "X %"
    else:
        caption = f"🟢 {update_data['slippage']}%"
    slippage_x = types.InlineKeyboardButton(
        text=caption, callback_data='select slippage x')
# limit order
    limit_token_price_title = types.InlineKeyboardButton(
        '----- Token Price -----', callback_data='set title')
    if update_data['limit-token-price'] == 0:
        caption = "X"
    else:
        caption = f"{update_data['limit-token-price']}"
    limit_token_price_x = types.InlineKeyboardButton(
        text=caption, callback_data='select limit token price x')

    limit_taxes = []
    limit_tax_count = len(chain_taxes)
    for index in range(limit_tax_count):
        if index_data['tax'] == 100:
            caption = f'{chain_taxes[index]}%'
        else:
            caption = f'{" 🟢" if index == index_data['tax'] else ""} {
                chain_taxes[index]}%'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select limit tax {index}")
        limit_taxes.append(button)
    limit_tax_title = types.InlineKeyboardButton(
        '----- Tax -----', callback_data='set title')
    if update_data['limit-tax'] == 0:
        caption = "X %"
    else:
        caption = f"🟢 {update_data['limit-tax']}%"
    limit_tax_x = types.InlineKeyboardButton(
        text=caption, callback_data='select limit tax x')

    market_capitals = []
    market_capital_count = len(chain_market_caps)
    for index in range(market_capital_count):
        if index_data['market_cap'] == 100:
            caption = f'{chain_market_caps[index]}'
        else:
            caption = f'{" 🟢" if index == index_data['market_cap'] else ""} {
                chain_market_caps[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select market capital {index}")
        market_capitals.append(button)
    market_capital_title = types.InlineKeyboardButton(
        '-----Max Market Capital -----', callback_data='set title')
    if update_data['market-capital'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['market-capital']}"
    market_capital_x = types.InlineKeyboardButton(
        text=caption, callback_data='select market capital x')

    liquidities = []
    liquidity_count = len(chain_liquidities)
    for index in range(liquidity_count):
        if index_data['liquidity'] == 100:
            caption = f'{chain_liquidities[index]}'
        else:
            caption = f'{" 🟢" if index == index_data['liquidity'] else ""} {
                chain_liquidities[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select liquidity {index}")
        liquidities.append(button)
    liquidity_title = types.InlineKeyboardButton(
        '-----Min Liquidity -----', callback_data='set title')
    if update_data['liquidity'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['liquidity']}"
    liquidity_x = types.InlineKeyboardButton(
        text=caption, callback_data='select liquidity x')

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
        '-----Intervals -----', callback_data='set title')
    if update_data['interval'] == 0:
        caption = "X min"
    else:
        caption = f"🟢 {update_data['interval']} min"
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
        '-----Times-----', callback_data='set title')
    if update_data['duration'] == 0:
        caption = "X d"
    else:
        caption = f"🟢 {update_data['duration']}"
    duration_x = types.InlineKeyboardButton(
        text=caption, callback_data='select duration x')

    dca_max_prices = []
    for index in range(len(chain_dca_max_prices)):
        if index_data['max_dca_price'] == 100:
            caption = f'{chain_dca_max_prices[index]}'
        else:
            caption = f'{" 🟢" if index == index_data['max_dca_price'] else ""} {
                chain_dca_max_prices[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select max price {index}")
        dca_max_prices.append(button)
    dca_max_price_title = types.InlineKeyboardButton(
        '----- Max Price -----', callback_data='set title')
    if update_data['dca-max-price'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['dca-max-price']}"
    dca_max_price_x = types.InlineKeyboardButton(
        text=caption, callback_data='select max price x')

    dca_min_prices = []
    for index in range(len(chain_dca_min_prices)):
        if index_data['min_dca_price'] == 100:
            caption = f'{chain_dca_min_prices[index]}'
        else:
            caption = f'{" 🟢" if index == index_data['min_dca_price'] else ""} {
                chain_dca_min_prices[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select min price {index}")
        dca_min_prices.append(button)
    dca_min_price_title = types.InlineKeyboardButton(
        '-----Min Price -----', callback_data='set title')
    if update_data['dca-min-price'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['dca-min-price']}"
    dca_min_price_x = types.InlineKeyboardButton(
        text=caption, callback_data='select min price x')

    create_order = types.InlineKeyboardButton(
        '✔️ Buy', callback_data='make buy order')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(*wallets[0:(wallet_count)])

    keyboard.row(*buys[0:(buy_count // 2)])
    keyboard.row(*buys[(buy_count // 2):buy_count], buy_x)

    current_chain_index = main_api.get_chain(chat_id)
    chains = main_api.get_chains()
    current_chain = chains[current_chain_index]
    if order_name == "Market Order":
        if current_chain == 'ethereum':
            keyboard.row(gas_amount_title)
            keyboard.row(*gas_amounts[0:(len(gas_amounts))], gas_amount_x)
            keyboard.row(gas_price_title)
            keyboard.row(*gas_prices[0:(len(gas_prices))], gas_price_x)
        keyboard.row(slippage_title, *
                     slippages[0:(len(slippages))], slippage_x)
        keyboard.row(anti_mev, anti_rug)
    elif order_name == "Limit Order":
        keyboard.row(limit_token_price_title, limit_token_price_x)
        keyboard.row(market_capital_title)
        keyboard.row(
            *market_capitals[0:(len(market_capitals))], market_capital_x)
        keyboard.row(liquidity_title)
        keyboard.row(
            *liquidities[0:(len(liquidities))], liquidity_x)
        keyboard.row(slippage_title, *
                     slippages[0:(len(slippages))], slippage_x)
    elif order_name == "DCA Order":
        keyboard.row(interval_title)
        keyboard.row(
            *intervals[0:(len(intervals))], interval_x)
        keyboard.row(duration_title)
        keyboard.row(
            *durations[0:(len(durations))], duration_x)
        keyboard.row(dca_min_price_title)
        keyboard.row(
            *dca_min_prices[0:(len(dca_min_prices))], dca_min_price_x)
        keyboard.row(dca_max_price_title)
        keyboard.row(
            *dca_max_prices[0:(len(dca_max_prices))], dca_max_price_x)
    keyboard.row(create_order)
    keyboard.row(back, close)

    return keyboard


def handle_input_token(bot, message):
   # user = user_model.get_user_by_telegram(message.chat.id)

    result['token'] = message.text
    chain = 'ethereum'
    token = result['token']
    name = "elo"

    text = f'''
            *Token Buy*

    Sell your tokens here.

  *{name}  (🔗{chain})*
  {message.text}
  ❌ Snipe not set

  [Scan](https://etherscan.io/address/{token}) | [Dexscreener](https://dexscreener.com/ethereum/{token}) | [DexTools](https://www.dextools.io/app/en/ether/pair-explorer/{token}) | [Defined](https://www.defined.fi/eth/{token})
      '''
    order_index = order_list[0]['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def select_buy_wallet(bot, message, index):
   # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]'
    index_list['wallet'] = int(index)
    result['wallet'] = int(index)
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


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
    result['gas_amount'] = chain_gas_amounts[int(index)]
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


def select_gas_price(bot, message, index):
    # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    index_list['gas_price'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['gas_price'] = chain_gas_prices[int(index)]
    x_value_list['gas-price'] = 0
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


def select_limit_token_price(bot, message, index):
    # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    index_list['limit_token_price'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['limit_token_price'] = chain_limit_token_prices[int(index)]
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    x_value_list['limit-token-price'] = 0
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
    result['interval'] = chain_intervals[int(index)]
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
    result['duration'] = chain_durations[int(index)]
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
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)~
    result['max_dca_price'] = chain_dca_max_prices[int(index)]
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
    result['min_dca_price'] = chain_dca_min_prices[int(index)]
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
*Token Buy > 💰 XΞ*
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


def handle_gas_price_x(bot, message):
    text = '''
*Token Buy > ⛽ X*
Enter the gas price to set:
'''
    item = "Gas Price"
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
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    for order in order_list:
        if order['active'] == True:
            order_index = order['name']
    keyboard = get_keyboard(order_index, x_value_list,
                            message.chat.id, index_list)
    token = 0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7

    chain = 'ethereum'

    name = "elo"
    text = f'''
            *Token Buy*

    Sell your tokens here.

     *{name}  (🔗{chain})*
      {token}
      ❌ Snipe not set

      [Scan](https://etherscan.io/address/{token}) | [Dexscreener](https://dexscreener.com/ethereum/{token}) | [DexTools](https://www.dextools.io/app/en/ether/pair-explorer/{token}) | [Defined](https://www.defined.fi/eth/{token})
          '''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def handle_buy_amount(bot, message, amount):
    order_amount = amount


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
        tx_hash = main_api.market_buy(message.chat.id, result['token'], buy_amount, result['slippage'], buy_wallet)
        print(tx_hash)
    elif order_name == "Limit Order":
        main_api.add_limit_order(message.chat.id, result['type'], result['token'], result['buy_amount'], result['slippage'], result['wallet'], result['limit_token_price'])
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
