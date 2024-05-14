from telebot import types

from src.database import user as user_model
from src.engine import main as engine
import config

order_index = "Market Order"


def handle_seller(bot, message):
    wallet_count = 4
    buy_amounts = [0.01, 0.02, 0.05, 0.1]
    buy_count = len(buy_amounts)

    keyboard = types.InlineKeyboardMarkup()

    market_order = types.InlineKeyboardButton(
        '✅ ① Market Order', callback_data='sell-market-orders')
    limit_order = types.InlineKeyboardButton(
        '② Limit Order', callback_data='sell-limit-orders')
    dca_order = types.InlineKeyboardButton(
        '③ DCA Order', callback_data='sell-dca-orders')

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
            f'💰 {buy_amount}Ξ', callback_data=f'auto buy {buy_amount}'))

    slippages = []
    for slippage_amount in config.SLIP_PAGE:
        slippages.append(types.InlineKeyboardButton(
            f'{slippage_amount}% Slippage', callback_data=f'select slippage'))

    buy_x = types.InlineKeyboardButton('💰 XΞ', callback_data='auto buy x')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(*wallets[0:(wallet_count // 2)])
    keyboard.row(*wallets[(wallet_count // 2):wallet_count])
    keyboard.row(wallet_all)

    keyboard.row(gas_max_price, gas_max_amount)

    keyboard.row(*slippages[(len(slippages) // 4):len(slippages)])

    # keyboard.row(anti_mev, anti_rug)
    keyboard.row(*buys[0:(buy_count // 2)])
    keyboard.row(*buys[(buy_count // 2):buy_count])
    keyboard.row(buy_x)
    keyboard.row(back, close)

    text = f'''Token Sell {order_index}'''
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id, text=text, parse_mode='Markdown')
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def handle_toggle_wallet(bot, message, index):
    user = user_model.get_user_by_telegram(message.chat.id)
    chain = user.chain
    wallets = user.wallets[chain]

    if index == 'all':
        active_all = True
        for wallet in wallets:
            if wallet['active'] == False:
                active_all = False
                break

        active = not active_all
        for index in range(len(wallets)):
            wallets[index]['active'] = active
    else:
        index = int(index)
        wallets[index]['active'] = not wallets[index]['active']

    user_model.update_user_by_id(user.id, 'wallets', user.wallets)

    keyboard = get_keyboard(wallets)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def handle_buy_x(bot, message):
    text = '''
*Token Buy > 💰 XΞ*
Enter the amount to buy:
'''

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_buy_x(bot, next_message))


def handle_input_buy_x(bot, message):
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

    text = f'''Token Sell {order_index}'''

    market_order = types.InlineKeyboardButton(
        '① Market Order', callback_data='sell-market-orders')
    limit_order = types.InlineKeyboardButton(
        '✅ ② Limit Order', callback_data='sell-limit-orders')
    dca_order = types.InlineKeyboardButton(
        '③ DCA Order', callback_data='sell-dca-orders')

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

   # keyboard.row(maximum_market_capital, minimum_liquidity)
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
    text = f'''Token Sell {order_index}'''

    market_order = types.InlineKeyboardButton(
        '✅ ① Market Order', callback_data='sell-market-orders')
    limit_order = types.InlineKeyboardButton(
        '② Limit Order', callback_data='sell-limit-orders')
    dca_order = types.InlineKeyboardButton(
        '③ DCA Order', callback_data='sell-dca-orders')

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

   # keyboard.row(anti_mev, anti_rug)

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
    text = f'''Token Sell {order_index}'''

    market_order = types.InlineKeyboardButton(
        '① Market Order', callback_data='sell-market-orders')
    limit_order = types.InlineKeyboardButton(
        '② Limit Order', callback_data='sell-limit-orders')
    dca_order = types.InlineKeyboardButton(
        '✅ ③ DCA Order', callback_data='sell-dca-orders')

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
