from telebot import types

from src.database import user as user_model
from src.engine import main as engine
import config

order_index = "Market Order"
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
gas_amount_list = [
    {"amount": "0.1", "active": False},
    {"amount": "0.3", "active": False},
    {"amount": "0.5", "active": False}
]
gas_price_list = [
    {"amount": "0.1", "active": False},
    {"amount": "0.3", "active": False},
    {"amount": "0.5", "active": False}
]
slip_page_list = [
    {"amount": "5", "active": False},
    {"amount": "10", "active": False},
    {"amount": "20", "active": False}
]

buy_amount_x = 0
gas_amount_x = 0
gas_price_x = 0
slip_page_x = 0


def handle_buyer(bot, message):
    user_model.create_user_by_telegram(message.chat.id)

    text = '''
*Token Buy*
Paste in a token address below to setup auto sniper for new launching token.
e.g. 0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7
    '''

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_token(bot, next_message))


def get_keyboard():
    wallet_count = 4
    buy_count = 4
    gas_amount_count = 3
    gas_price_count = 3
    slip_page_count = 3

    keyboard = types.InlineKeyboardMarkup()

    market_order = types.InlineKeyboardButton(
        '✅ Market', callback_data='buy-market-orders')
    limit_order = types.InlineKeyboardButton(
        'Limit', callback_data='buy-limit-orders')
    dca_order = types.InlineKeyboardButton(
        'DCA', callback_data='buy-dca-orders')

    keyboard.row(market_order, limit_order, dca_order)

    wallets = []
    for index in range(wallet_count):
        caption = f'{" 🟢" if main_wallets[index]['active'] == True else ""} W{
            index + 1}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select buy wallet {index}")
        wallets.append(button)
    wallet_all = types.InlineKeyboardButton(
        'All Wallets', callback_data=f'select buy wallet all')

    anti_mev = types.InlineKeyboardButton(
        '🔴 Anti-Mev', callback_data=f'anti mev')
    anti_rug = types.InlineKeyboardButton(
        '🔴 Anti-Rug', callback_data=f'anti Rug')

    buys = []
    for index in range(buy_count):
        caption = f'{" 🟢" if buy_amount_list[index]['active'] == True else ""} 💰{
            buy_amount_list[index]['amount']}Ξ'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select buy amount {index}")
        buys.append(button)
    buy_x = types.InlineKeyboardButton(
        '💰 XΞ', callback_data='select buy amount x')

    gas_amounts = []
    for index in range(gas_amount_count):
        caption = f'{" 🟢" if gas_amount_list[index]['active'] == True else ""} {
            gas_amount_list[index]['amount']}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select gas amount {index}")
        gas_amounts.append(button)
    gas_amount_x = types.InlineKeyboardButton(
        'GasAmount ✏️', callback_data='select gas amount x')

    gas_prices = []
    for index in range(gas_price_count):
        caption = f'{" 🟢" if gas_price_list[index]['active'] == True else ""} {
            gas_price_list[index]['amount']}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select gas price {index}")
        gas_prices.append(button)
    gas_price_x = types.InlineKeyboardButton(
        'GasPrice ✏️', callback_data='select gas price x')

    slippages = []
    for index in range(slip_page_count):
        caption = f'{" 🟢" if slip_page_list[index]['active'] == True else ""} {
            slip_page_list[index]['amount']}%'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"select slippage {index}")
        slippages.append(button)
    slippage_x = types.InlineKeyboardButton(
        'Slippage ✏️', callback_data='select slippage x')

    create_order = types.InlineKeyboardButton(
        '✔️ Buy', callback_data='make buy order')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(*wallets[0:(wallet_count // 2)])
    keyboard.row(*wallets[(wallet_count // 2):wallet_count])
    keyboard.row(wallet_all)

    keyboard.row(*buys[0:(buy_count // 2)])
    keyboard.row(*buys[(buy_count // 2):buy_count], buy_x)

    keyboard.row(gas_amount_x, *
                 gas_amounts[(len(gas_amounts) // 4):len(gas_amounts)])
    keyboard.row(gas_price_x, *
                 gas_prices[(len(gas_prices) // 4):len(gas_prices)])

    keyboard.row(slippage_x, *slippages[(len(slippages) // 4):len(slippages)])

    keyboard.row(anti_mev, anti_rug)
    keyboard.row(create_order)
    keyboard.row(back, close)

    return keyboard


def handle_input_token(bot, message):
    user = user_model.get_user_by_telegram(message.chat.id)

    token = 0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7

    chain = 'ethereum'

    name = "elo"

    text = f'''
  *{name}  (🔗{chain})*
  {token}
  ❌ Snipe not set

  [Scan](https://etherscan.io/address/{token}) | [Dexscreener](https://dexscreener.com/ethereum/{token}) | [DexTools](https://www.dextools.io/app/en/ether/pair-explorer/{token}) | [Defined](https://www.defined.fi/eth/{token})
      '''

    keyboard = get_keyboard()
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def select_buy_wallet(bot, message, index):
    user = user_model.get_user_by_telegram(message.chat.id)
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

   # user_model.update_user_by_id(user.id, 'wallets', user.wallets)

    keyboard = get_keyboard()

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_buy_amount(bot, message, index):
    user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    for amount in buy_amount_list:
        amount['active'] = False
    index = int(index)
    buy_amount_list[index]['active'] = True
  #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)

    keyboard = get_keyboard()

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_gas_amount(bot, message, index):
    user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    for amount in gas_amount_list:
        amount['active'] = False
    index = int(index)
    gas_amount_list[index]['active'] = True
  #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)

    keyboard = get_keyboard()

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_gas_price(bot, message, index):
    user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    for amount in gas_price_list:
        amount['active'] = False
    index = int(index)
    gas_price_list[index]['active'] = True
  #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)

    keyboard = get_keyboard()

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_slip_page(bot, message, index):
    user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    for amount in slip_page_list:
        amount['active'] = False
    index = int(index)
    slip_page_list[index]['active'] = True
  #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)

    keyboard = get_keyboard()

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def handle_buy_amount_x(bot, message):
    text = '''
*Token Buy > 💰 XΞ*
Enter the amount to buy:
'''

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_buy_amount_x(bot, next_message))


def handle_input_buy_amount_x(bot, message):
    amount = float(message.text)
    handle_buy_amount(bot, message, amount)


def handle_buy_amount(bot, message, amount):
    order_amount = amount


def handle_buy(bot, message):
    bot.send_message(chat_id=message.chat.id,
                     text='Successfully registered Order')


def handle_limit_order(bot, message):
    order_index = "Limit Order"
    wallet_count = 4
    buy_amounts = [0.01, 0.02, 0.05, 0.1]
    buy_count = len(buy_amounts)

    keyboard = types.InlineKeyboardMarkup()

    token = 0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7
    text = f'''
*elon  (🔗ethereum)*
0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7
❌ Snipe not set

[Scan](https://etherscan.io/address/{token}) | [Dexscreener](https://dexscreener.com/ethereum/{token}) | [DexTools](https://www.dextools.io/app/en/ether/pair-explorer/{token}) | [Defined](https://www.defined.fi/eth/{token})
    '''

    market_order = types.InlineKeyboardButton(
        'Market Order', callback_data='buy-market-orders')
    limit_order = types.InlineKeyboardButton(
        '✅ Limit Order', callback_data='buy-limit-orders')
    dca_order = types.InlineKeyboardButton(
        'DCA Order', callback_data='buy-dca-orders')

    keyboard.row(market_order, limit_order, dca_order)

    wallets = []
    for index in range(wallet_count):
        caption = f'''W{index}'''
        button = types.InlineKeyboardButton(
            text=caption, callback_data="auto all")
        wallets.append(button)
    wallet_all = types.InlineKeyboardButton(
        'All Wallets', callback_data=f'auto wallet all')
# Limit Order
    limit_token_price = types.InlineKeyboardButton(
        'Token Price', callback_data=f'limit token price')
    maximum_market_capital = types.InlineKeyboardButton(
        'Maximum Market Capital', callback_data=f'maximum market capital')
    minimum_liquidity = types.InlineKeyboardButton(
        'Minimum Liquidity', callback_data=f'minimum liquidity')
    buy_sell_tax = types.InlineKeyboardButton(
        'Buy/Sell Tax', callback_data=f'buy sell tax')
    stop_loss = types.InlineKeyboardButton(
        'Stop Loss', callback_data=f'stop loss')

    buys = []
    for buy_amount in buy_amounts:
        buys.append(types.InlineKeyboardButton(
            f'💰 {buy_amount}Ξ', callback_data=f'buy amount {buy_amount}'))
    buy_x = types.InlineKeyboardButton('💰 XΞ', callback_data='buy amount x')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    create_order = types.InlineKeyboardButton(
        '✔️ Make Order', callback_data='make order')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(*wallets[0:(wallet_count // 2)])
    keyboard.row(*wallets[(wallet_count // 2):wallet_count])
    keyboard.row(wallet_all)

    keyboard.row(maximum_market_capital, minimum_liquidity)
    keyboard.row(buy_sell_tax, limit_token_price, stop_loss)

    keyboard.row(*buys[0:(buy_count // 2)])
    keyboard.row(*buys[(buy_count // 2):buy_count])
    keyboard.row(buy_x)
    keyboard.row(create_order)
    keyboard.row(back, close)

    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id, text=text, parse_mode='Markdown')
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def handle_market_order(bot, message):
    order_index = "Market Order"
    wallet_count = 4
    buy_amounts = [0.01, 0.02, 0.05, 0.1]
    buy_count = len(buy_amounts)

    keyboard = types.InlineKeyboardMarkup()

    token = 0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7
    text = f'''
*elon  (🔗ethereum)*
0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7
❌ Snipe not set

[Scan](https://etherscan.io/address/{token}) | [Dexscreener](https://dexscreener.com/ethereum/{token}) | [DexTools](https://www.dextools.io/app/en/ether/pair-explorer/{token}) | [Defined](https://www.defined.fi/eth/{token})
    '''

    market_order = types.InlineKeyboardButton(
        '✅ Market Order', callback_data='buy-market-orders')
    limit_order = types.InlineKeyboardButton(
        'Limit Order', callback_data='buy-limit-orders')
    dca_order = types.InlineKeyboardButton(
        'DCA Order', callback_data='buy-dca-orders')

    keyboard.row(market_order, limit_order, dca_order)

    wallets = []
    for index in range(wallet_count):
        caption = f'''W{index}'''
        button = types.InlineKeyboardButton(
            text=caption, callback_data="auto all")
        wallets.append(button)
    wallet_all = types.InlineKeyboardButton(
        'All Wallets', callback_data=f'auto wallet all')
# Market Order
    gas_max_price = types.InlineKeyboardButton(
        'Gas Max Price', callback_data=f'gas max price')
    gas_max_amount = types.InlineKeyboardButton(
        'Gas Max Amount', callback_data=f'gas max amount')
    anti_mev = types.InlineKeyboardButton(
        'Anti-Mev', callback_data=f'anti mev')
    anti_rug = types.InlineKeyboardButton(
        'Anti-Rug', callback_data=f'anti Rug')

    buys = []
    for buy_amount in buy_amounts:
        buys.append(types.InlineKeyboardButton(
            f'💰 {buy_amount}Ξ', callback_data=f'buy amount {buy_amount}'))

    slippages = []
    for slippage_amount in config.SLIP_PAGE:
        slippages.append(types.InlineKeyboardButton(
            f'{slippage_amount}% Slippage', callback_data=f'select slippage'))
    buy_x = types.InlineKeyboardButton('💰 XΞ', callback_data='buy amount x')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    create_order = types.InlineKeyboardButton(
        '✔️ Make Order', callback_data='make order')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(*wallets[0:(wallet_count // 2)])
    keyboard.row(*wallets[(wallet_count // 2):wallet_count])
    keyboard.row(wallet_all)

    keyboard.row(gas_max_price, gas_max_amount)

    keyboard.row(anti_mev, anti_rug)

    keyboard.row(*buys[0:(buy_count // 2)])
    keyboard.row(*buys[(buy_count // 2):buy_count])
    keyboard.row(buy_x)
    keyboard.row(create_order)
    keyboard.row(back, close)

    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id, text=text, parse_mode='Markdown')
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def handle_dca_order(bot, message):
    order_index = "DCA Order"
    wallet_count = 4
    period_count = 4

    buy_amounts = [0.01, 0.02, 0.05, 0.1]
    buy_count = len(buy_amounts)

    keyboard = types.InlineKeyboardMarkup()

    token = 0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7
    text = f'''
*elon  (🔗ethereum)*
0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7
❌ Snipe not set

[Scan](https://etherscan.io/address/{token}) | [Dexscreener](https://dexscreener.com/ethereum/{token}) | [DexTools](https://www.dextools.io/app/en/ether/pair-explorer/{token}) | [Defined](https://www.defined.fi/eth/{token})
    '''

    market_order = types.InlineKeyboardButton(
        'Market Order', callback_data='buy-market-orders')
    limit_order = types.InlineKeyboardButton(
        'Limit Order', callback_data='buy-limit-orders')
    dca_order = types.InlineKeyboardButton(
        '✅ DCA Order', callback_data='buy-dca-orders')

    keyboard.row(market_order, limit_order, dca_order)

    wallets = []
    for index in range(wallet_count):
        caption = f'''W{index}'''
        button = types.InlineKeyboardButton(
            text=caption, callback_data="auto all")
        wallets.append(button)
    wallet_all = types.InlineKeyboardButton(
        'All Wallets', callback_data=f'auto wallet all')
# DCA Order
    dca_max_price = types.InlineKeyboardButton(
        'Max Price', callback_data=f'dca max price')
    dca_min_price = types.InlineKeyboardButton(
        'Min Price', callback_data=f'dca min price')
    dca_token_price = types.InlineKeyboardButton(
        'Token Amount', callback_data=f'dca token amount')
    dca_period = types.InlineKeyboardButton(
        'Period', callback_data=f'dca period button')
    dca_times = types.InlineKeyboardButton(
        'Times', callback_data=f'dca times')

    periods = []
    for index in config.DCA_PERIOD:
        caption = f'''⏰ {index}'''
        button = types.InlineKeyboardButton(
            text=caption, callback_data="dca period ")
        periods.append(button)

    period_x = types.InlineKeyboardButton('⏰ X', callback_data='dca period x')
    periods.append(period_x)

    buys = []
    for buy_amount in buy_amounts:
        buys.append(types.InlineKeyboardButton(
            f'💰 {buy_amount}Ξ', callback_data=f'buy amount {buy_amount}'))
    buy_x = types.InlineKeyboardButton('💰 XΞ', callback_data='buy amount x')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    create_order = types.InlineKeyboardButton(
        '✔️ Make Order', callback_data='make order')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(*wallets[0:(wallet_count // 2)])
    keyboard.row(*wallets[(wallet_count // 2):wallet_count])
    keyboard.row(wallet_all)

    keyboard.row(dca_token_price, dca_min_price, dca_max_price)
    keyboard.row(*periods[(period_count // 5):period_count])

    keyboard.row(*buys[0:(buy_count // 2)])
    keyboard.row(*buys[(buy_count // 2):buy_count])
    keyboard.row(buy_x)
    keyboard.row(create_order)
    keyboard.row(back, close)

    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id, text=text, parse_mode='Markdown')
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
