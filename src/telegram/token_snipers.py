from telebot import types
from src.engine import api as main_api

current_token_sniper = {'index': 0}
updat_values = {'id': 0, 'token': "", 'buy_amount': 0, 'gas': 0, 'slippage': 0, 'limit_token_price': 0,
                'tax': 0, 'market_cap': 0, 'liquidity': 0, 'wallet': 0, 'tx_hash': ''}


def get_keyboard(chat_id, order, order_index):
    keyboard = types.InlineKeyboardMarkup()
    updat_values.update(order)
    index_button = types.InlineKeyboardButton(
        f'Order: {order_index + 1}', callback_data='aaa')
    token = types.InlineKeyboardButton(
        f'Token: {order['token']}', callback_data='aaa')
    wallet = types.InlineKeyboardButton(
        f'Wallet: W{order['wallet']}', callback_data='aaa')
    amount = types.InlineKeyboardButton(
        f'Buy Amount: {order['buy_amount']}E', callback_data='handle_token_sniper_input buy_amount')
    gas = types.InlineKeyboardButton(
        f'Gas: {order['gas']}', callback_data='handle_token_sniper_input gas')
    slippage = types.InlineKeyboardButton(
        f'Slippage: {order['slippage']}%', callback_data='handle_token_sniper_input slippage')
    limit_token_price = types.InlineKeyboardButton(
        f'Token Price: {order['limit_token_price']}', callback_data='handle_token_sniper_input limit_token_price')
    tax = types.InlineKeyboardButton(
        f'Tax: {order['tax']}%', callback_data='handle_token_sniper_input tax')
    market_cap = types.InlineKeyboardButton(
        f'MaxCap: {order['market_cap']}', callback_data='handle_token_sniper_input market_cap')
    liquidity = types.InlineKeyboardButton(
        f'Liq: {order['liquidity']}', callback_data='handle_token_sniper_input liquidity')
    left_button = types.InlineKeyboardButton(
        '<<', callback_data='handle_prev_token_sniper')
    right_button = types.InlineKeyboardButton(
        '>>', callback_data='handle_next_token_sniper')
    update = types.InlineKeyboardButton(
        'Update', callback_data='handle_update_token_sniper')
    cancel = types.InlineKeyboardButton(
        'Cancel Order', callback_data='handle_remove_token_sniper')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')

    keyboard.row(left_button, index_button, right_button)
    keyboard.row(token, wallet, amount)
    keyboard.row(gas, slippage)
    keyboard.row(limit_token_price, tax)
    keyboard.row(market_cap, liquidity)
    keyboard.row(update, cancel)
    keyboard.row(back, close)
    return keyboard


def handle_orders(bot, message):
    token_snipers = main_api.get_token_snipers(message.chat.id)
    text = f'''
*Token Snipers*

You currently have {len(token_snipers)} snipers. You can manage your orders here.

Your orders are:
    '''
    if len(token_snipers) == 0:
        bot.send_message(chat_id=message.chat.id, text='You have no orders')
    else:
        order = token_snipers[current_token_sniper['index']]
        keyboard = get_keyboard(message.chat.id, order,
                                current_token_sniper['index'])
        bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                         reply_markup=keyboard, disable_web_page_preview=True)


def handle_next_order(bot, message):
    index = current_token_sniper['index']
    index += 1
    current_token_sniper['index'] = index
    token_snipers = main_api.get_token_snipers(message.chat.id)

    order = token_snipers[index]
    text = f'''
*limit Orders*

You currently have {len(token_snipers)} limit orders. You can manage your orders here.

Your orders are:
    '''
    keyboard = get_keyboard(message.chat.id, order, index)
    bot.delete_message(chat_id=message.chat.id,
                       message_id=message.message_id)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def handle_prev_order(bot, message):
    token_snipers = main_api.get_token_snipers(message.chat.id)
    index = current_token_sniper['index']
    index -= 1
    current_token_sniper['index'] = index
    order = token_snipers[index]
    text = f'''
*limit Orders*

You currently have {len(token_snipers)} limit orders. You can manage your orders here.

Your orders are:
    '''
    keyboard = get_keyboard(message.chat.id, order, index)
    bot.delete_message(chat_id=message.chat.id,
                       message_id=message.message_id)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def handle_remove_order(bot, message):
    orders = main_api.get_token_snipers(message.chat.id)
    index = current_token_sniper['index']
    tx_hash = orders[index]['tx_hash']
    main_api.remove_token_sniper(message.chat.id, tx_hash)
    bot.send_message(chat_id=message.chat.id,
                     text="Successfully cancelled order!!!")
    handle_orders(bot, message)


def handle_input(bot, message, item):
    text = '''
*Update Order*
Enter the value to change:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_update_order(bot, message):
    main_api.update_token_sniper(message.chat.id, updat_values)
    bot.send_message(chat_id=message.chat.id,
                     text="Successfully updated order!!!")


def handle_input_value(bot, message, item):
    orders = main_api.get_token_snipers(message.chat.id)
    index = current_token_sniper['index']
    order = orders[index]
    updat_values[item] = message.text
    text = f'''
*limit Orders*

You currently have {len(orders)} limit orders. You can manage your orders here.

Your orders are:
    '''
    keyboard = get_keyboard(message.chat.id, updat_values, index)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
