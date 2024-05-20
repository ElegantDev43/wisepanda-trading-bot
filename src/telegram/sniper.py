from telebot import types

from src.database import user as user_model

main_wallets = [
    {"address": "Leo", "active": False, "age": 25},
    {"address": "Tim", "active": False, "age": 23},
    {"address": "Alice", "active": False, "age": 31},
    {"address": "Jack", "active": False, "age": 27}
]
buy_amount_list = [
    {"amount": "0.1", "active": False},
    {"amount": "0.3", "active": False},
    {"amount": "0.5", "active": False},
    {"amount": "1", "active": False}
]

token_price_list = [
    {"amount": "5", "active": False},
    {"amount": "10", "active": False},
    {"amount": "20", "active": False}
]

market_capital_list = [
    {"amount": "5", "active": False},
    {"amount": "10", "active": False},
    {"amount": "20", "active": False}
]

liquidity_list = [
    {"amount": "5", "active": False},
    {"amount": "10", "active": False},
    {"amount": "20", "active": False}
]

tax_list = [
    {"amount": "5", "active": False},
    {"amount": "10", "active": False},
    {"amount": "20", "active": False}
]
x_value_list = {"buy-amount": 0, "gas-amount": 0, "gas-price": 0, "limit-token-price": 0,
                "slippage": 0, "market-capital": 0, "liquidity": 0, "limit-tax": 0}


def initialize_all():
    for index in main_wallets:
        index['active'] = False
    for index in buy_amount_list:
        index['active'] = False


def initialize_x_value():
    x_value_list['buy-amount'] = 0
    x_value_list['gas-amount'] = 0
    x_value_list['gas-price'] = 0
    x_value_list['limit-token-price'] = 0
    x_value_list['slippage'] = 0
    x_value_list['market-capital'] = 0
    x_value_list['liquidity'] = 0
    x_value_list['limit-tax'] = 0


def handle_sniper(bot, message):
   # user_model.create_user_by_telegram(message.chat.id)
    initialize_all()
    text = '''
 🎯 *Token Sniper*

Enter a token symbol or address to buy.
    '''

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_token(bot, next_message))


def get_keyboard(update_data):
    wallet_count = 4
    buy_count = 4

    keyboard = types.InlineKeyboardMarkup()
    wallets = []
    for index in range(wallet_count):
        caption = f'{" 🟢" if main_wallets[index]['active'] == True else ""} W{
            index + 1}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select buy wallet {index}")
        wallets.append(button)
    wallet_all = types.InlineKeyboardButton(
        'All Wallets', callback_data=f'sniper select buy wallet all')

    buys = []
    for index in range(buy_count):
        caption = f'{" 🟢" if buy_amount_list[index]['active'] == True else ""} 💰{
            buy_amount_list[index]['amount']}Ξ'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select buy amount {index}")
        buys.append(button)

    if update_data['buy-amount'] == 0:
        caption = "💰 XΞ"
    else:
        caption = f"🟢 💰 {update_data['buy-amount']}Ξ"
    buy_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select buy amount x')
# limit order
    limit_token_prices = []
    for index in range(3):
        caption = f'{" 🟢" if token_price_list[index]['active'] == True else ""} {
            token_price_list[index]['amount']}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select limit token price {index}")
        limit_token_prices.append(button)
    limit_token_price_title = types.InlineKeyboardButton(
        'TP :', callback_data='set title')
    if update_data['limit-token-price'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['limit-token-price']}"
    limit_token_price_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select limit token price x')

    limit_taxes = []
    for index in range(3):
        caption = f'{" 🟢" if tax_list[index]['active'] == True else ""} {
            tax_list[index]['amount']}%'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select limit tax {index}")
        limit_taxes.append(button)
    limit_tax_title = types.InlineKeyboardButton(
        'Tax :', callback_data='set title')
    if update_data['limit-tax'] == 0:
        caption = "X %"
    else:
        caption = f"🟢 {update_data['limit-tax']}%"
    limit_tax_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select limit tax x')

    market_capitals = []
    for index in range(3):
        caption = f'{" 🟢" if market_capital_list[index]['active'] == True else ""} {
            market_capital_list[index]['amount']}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select market capital {index}")
        market_capitals.append(button)
    market_capital_title = types.InlineKeyboardButton(
        'Max MC :', callback_data='set title')
    if update_data['market-capital'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['market-capital']}"
    market_capital_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select market capital x')

    liquidities = []
    for index in range(3):
        caption = f'{" 🟢" if liquidity_list[index]['active'] == True else ""} {
            liquidity_list[index]['amount']}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select liquidity {index}")
        liquidities.append(button)
    liquidity_title = types.InlineKeyboardButton(
        'Min Liq :', callback_data='set title')
    if update_data['liquidity'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['liquidity']}"
    liquidity_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select liquidity x')

    create_order = types.InlineKeyboardButton(
        '✔️ Buy', callback_data='make buy order')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(*wallets[0:(wallet_count // 2)])
    keyboard.row(*wallets[(wallet_count // 2):wallet_count])
    keyboard.row(wallet_all)

    keyboard.row(*buys[0:(buy_count // 2)])
    keyboard.row(*buys[(buy_count // 2):buy_count], buy_x)

    keyboard.row(limit_token_price_title)
    keyboard.row(
        *limit_token_prices[0:(len(limit_token_prices))], limit_token_price_x)
    keyboard.row(market_capital_title)
    keyboard.row(
        *market_capitals[0:(len(market_capitals))], market_capital_x)
    keyboard.row(liquidity_title)
    keyboard.row(
        *liquidities[0:(len(liquidities))], liquidity_x)
    keyboard.row(limit_tax_title)
    keyboard.row(
        *limit_taxes[0:(len(limit_taxes))], limit_tax_x)

    keyboard.row(create_order)
    keyboard.row(back, close)

    return keyboard


def handle_input_token(bot, message):
    # user = user_model.get_user_by_telegram(message.chat.id)

    token = 0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7

    chain = 'ethereum'

    name = "elo"

    text = f'''
  *{name}  (🔗{chain})*
  {token}
  ❌ Snipe not set

  [Scan](https://etherscan.io/address/{token}) | [Dexscreener](https://dexscreener.com/ethereum/{token}) | [DexTools](https://www.dextools.io/app/en/ether/pair-explorer/{token}) | [Defined](https://www.defined.fi/eth/{token})
      '''
    keyboard = get_keyboard(x_value_list)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def select_buy_wallet(bot, message, index):
    # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    if index == 'all':
        active_all = True
        for wallet in main_wallets:
            if wallet['active'] == False:
                active_all = False
                break

        active = not active_all
        for index in range(len(main_wallets)):
            main_wallets[index]['active'] = active
    else:
        index = int(index)
        main_wallets[index]['active'] = not main_wallets[index]['active']
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    keyboard = get_keyboard(x_value_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_buy_amount(bot, message, index):
    # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    for amount in buy_amount_list:
        amount['active'] = False
    index = int(index)
    buy_amount_list[index]['active'] = True
    x_value_list['buy-amount'] = 0

    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    keyboard = get_keyboard(x_value_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_limit_token_price(bot, message, index):
    # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    for amount in token_price_list:
        amount['active'] = False
    index = int(index)
    token_price_list[index]['active'] = True
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    x_value_list['limit-token-price'] = 0
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    keyboard = get_keyboard(x_value_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_limit_tax(bot, message, index):
    # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    x_value_list['limit-tax'] = 0
    for amount in tax_list:
        amount['active'] = False
    index = int(index)
    tax_list[index]['active'] = True
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    keyboard = get_keyboard(x_value_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_market_capital(bot, message, index):
    # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    x_value_list['market-capital'] = 0
    for amount in market_capital_list:
        amount['active'] = False
    index = int(index)
    market_capital_list[index]['active'] = True
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    keyboard = get_keyboard(x_value_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_liquidity(bot, message, index):
    # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    x_value_list['liquidity'] = 0
    for amount in liquidity_list:
        amount['active'] = False
    index = int(index)
    liquidity_list[index]['active'] = True
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    keyboard = get_keyboard(x_value_list)

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


def handle_input_value(bot, message, item):
    if item == "Buy Amount":
        buy_amount_x = float(message.text)
        x_value_list['buy-amount'] = buy_amount_x
        for index in buy_amount_list:
            index['active'] = False
    elif item == "Token Price":
        token_price_x = float(message.text)
        x_value_list['limit-token-price'] = token_price_x
        for index in token_price_list:
            index['active'] = False
    elif item == "Market Capital":
        market_capital_x = float(message.text)
        x_value_list['market-capital'] = market_capital_x
        for index in market_capital_list:
            index['active'] = False
    elif item == "Liquidity":
        slippage_x = float(message.text)
        x_value_list['liquidity'] = slippage_x
        for index in liquidity_list:
            index['active'] = False
    elif item == "Tax":
        slippage_x = float(message.text)
        x_value_list['limit-tax'] = slippage_x
        for index in tax_list:
            index['active'] = False
    order_index = ''
   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    keyboard = get_keyboard(x_value_list)
    token = 0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7

    chain = 'ethereum'

    name = "elo"
    text = f'''
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
    bot.send_message(chat_id=message.chat.id,
                     text='Successfully registered Order')
