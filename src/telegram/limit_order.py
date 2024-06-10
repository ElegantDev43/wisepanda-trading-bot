from telebot import types
from src.engine import api as main_api

current_limit_order = {'index': 0}
updat_values = {'id': 0, 'type': 0, 'tx_hash': '', 'token': "", 'buy_amount': 0, 'limit_token_price': 0,
                'tax': 0, 'stop-loss': 0, 'market_cap': 0, 'liquidity': 0, 'wallet': 0, 'thread_id': ''}


def get_keyboard(chat_id, order, order_index):
    keyboard = types.InlineKeyboardMarkup()
    updat_values.update(order)
    index_button = types.InlineKeyboardButton(
        f'Order: {order_index + 1}', callback_data='aaa')
    if order['type'] == 0:
        caption = 'Type: Buy'
    else:
        caption = 'Type: Sell'
    type = types.InlineKeyboardButton(caption, callback_data='aaa')
    token = types.InlineKeyboardButton(
        f'Token: {order['token']}', callback_data='aaa')
    wallet = types.InlineKeyboardButton(
        f'Wallet: W{order['wallet']}', callback_data='aaa')
    amount = types.InlineKeyboardButton(
        f'Buy Amount: {order['buy_amount']}E', callback_data='handle_limit_input buy_amount')
    limit_token_price = types.InlineKeyboardButton(
        f'Token Price: {order['limit_token_price']}', callback_data='handle_limit_input limit_token_price')
    stop_loss = types.InlineKeyboardButton(
        f'Stop Loss: {order['stop-loss']}%', callback_data='handle_limit_input stop-loss')
    tax = types.InlineKeyboardButton(
        f'Tax: {order['tax']}%', callback_data='handle_limit_input tax')
    market_cap = types.InlineKeyboardButton(
        f'MaxCap: {order['market_cap']}', callback_data='handle_limit_input market_cap')
    liquidity = types.InlineKeyboardButton(
        f'Liq: {order['liquidity']}', callback_data='handle_limit_input liquidity')
    left_button = types.InlineKeyboardButton(
        '<<', callback_data='handle_prev_limit_order')
    right_button = types.InlineKeyboardButton(
        '>>', callback_data='handle_next_limit_order')
    update = types.InlineKeyboardButton(
        'Update', callback_data='handle_update_limit_order')
    cancel = types.InlineKeyboardButton(
        'Cancel Order', callback_data='handle_remove_limit_order')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')

    keyboard.row(left_button, index_button, right_button)
    keyboard.row(type, token)
    if order['type'] == 1:
        keyboard.row(amount)
        keyboard.row(stop_loss, tax)
    else:
        keyboard.row(wallet, amount)
        keyboard.row(limit_token_price, tax)
    keyboard.row(market_cap, liquidity)
    keyboard.row(update, cancel)
    keyboard.row(back, close)
    return keyboard


def handle_orders(bot, message):
    limit_orders = main_api.get_limit_orders(message.chat.id)
    text = f'''
*limit Orders*

You currently have {len(limit_orders)} limit orders. You can manage your orders here.

Your orders are:
    '''
    if len(limit_orders) == 0:
        bot.send_message(chat_id=message.chat.id, text='You have no orders')
    else:
        order = limit_orders[current_limit_order['index']]
        keyboard = get_keyboard(message.chat.id, order,
                                current_limit_order['index'])
        bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                         reply_markup=keyboard, disable_web_page_preview=True)


def handle_next_order(bot, message):
    index = current_limit_order['index']
    index += 1
    current_limit_order['index'] = index
    limit_orders = main_api.get_limit_orders(message.chat.id)

    order = limit_orders[index]
    text = f'''
*limit Orders*

You currently have {len(limit_orders)} limit orders. You can manage your orders here.

Your orders are:
    '''
    keyboard = get_keyboard(message.chat.id, order, index)
    bot.delete_message(chat_id=message.chat.id,
                       message_id=message.message_id)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def handle_prev_order(bot, message):
    limit_orders = main_api.get_limit_orders(message.chat.id)
    index = current_limit_order['index']
    index -= 1
    current_limit_order['index'] = index
    order = limit_orders[index]
    text = f'''
*limit Orders*

You currently have {len(limit_orders)} limit orders. You can manage your orders here.

Your orders are:
    '''
    keyboard = get_keyboard(message.chat.id, order, index)
    bot.delete_message(chat_id=message.chat.id,
                       message_id=message.message_id)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def handle_remove_order(bot, message):
    orders = main_api.get_limit_orders(message.chat.id)
    index = current_limit_order['index']
    thread_id = orders[index]['thread_id']
    main_api.remove_limit_order(message.chat.id, thread_id)
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
    main_api.update_limit_order(message.chat.id, updat_values)
    bot.send_message(chat_id=message.chat.id,
                     text="Successfully updated order!!!")


def handle_input_value(bot, message, item):
    orders = main_api.get_limit_orders(message.chat.id)
    index = current_limit_order['index']
    order = orders[index]
    updat_values[item] = message.text
    thread_id = orders[index]['thread_id']
    updat_values['thread_id'] = thread_id
    text = f'''
*limit Orders*

You currently have {len(orders)} limit orders. You can manage your orders here.

Your orders are:
    '''
    keyboard = get_keyboard(message.chat.id, updat_values, index)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
