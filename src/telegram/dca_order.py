from telebot import types
from src.engine import api as main_api

current_dca_order = {'index': 0}
updat_values = {'id': 0, 'type': 0, 'tx_hash': '', 'token': "", 'buy_amount': 0, 'interval': 0,
                'duration': 0, 'min_dca_price': 0, 'max_dca_price': 0, 'wallet': 0}


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
        f'Buy Amount: {order['buy_amount']}E', callback_data='handle_dca_input buy_amount')
    interval = types.InlineKeyboardButton(
        f'Interval: {order['interval']}', callback_data='handle_dca_input interval')
    duration = types.InlineKeyboardButton(
        f'Times: {order['duration']}%', callback_data='handle_dca_input duration')
    min_dca_price = types.InlineKeyboardButton(
        f'Min Price: {order['min_dca_price']}', callback_data='handle_dca_input min_dca_price')
    max_dca_price = types.InlineKeyboardButton(
        f'Max Price: {order['max_dca_price']}', callback_data='handle_dca_input max_dca_price')
    left_button = types.InlineKeyboardButton(
        '<<', callback_data='handle_prev_dca_order')
    right_button = types.InlineKeyboardButton(
        '>>', callback_data='handle_next_dca_order')
    update = types.InlineKeyboardButton(
        'Update', callback_data='handle_update_dca_order')
    cancel = types.InlineKeyboardButton(
        'Cancel Order', callback_data='handle_remove_dca_order')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')

    keyboard.row(left_button, index_button, right_button)
    keyboard.row(type, token)
    keyboard.row(wallet, amount)
    keyboard.row(interval, duration)
    keyboard.row(min_dca_price, max_dca_price)
    keyboard.row(update, cancel)
    keyboard.row(back, close)
    return keyboard


def handle_orders(bot, message):
    dca_orders = main_api.get_dca_orders(message.chat.id)
    text = f'''
*dca Orders*

You currently have {len(dca_orders)} dca orders. You can manage your orders here.

Your orders are:
    '''
    if len(dca_orders) == 0:
        bot.send_message(chat_id=message.chat.id, text='You have no orders')
    else:
        order = dca_orders[current_dca_order['index']]
        keyboard = get_keyboard(message.chat.id, order,
                                current_dca_order['index'])
        bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                         reply_markup=keyboard, disable_web_page_preview=True)


def handle_next_order(bot, message):
    index = current_dca_order['index']
    index += 1
    current_dca_order['index'] = index
    dca_orders = main_api.get_dca_orders(message.chat.id)

    order = dca_orders[index]
    text = f'''
*dca Orders*

You currently have {len(dca_orders)} dca orders. You can manage your orders here.

Your orders are:
    '''
    keyboard = get_keyboard(message.chat.id, order, index)
    bot.delete_message(chat_id=message.chat.id,
                       message_id=message.message_id)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def handle_prev_order(bot, message):
    dca_orders = main_api.get_dca_orders(message.chat.id)
    index = current_dca_order['index']
    index -= 1
    current_dca_order['index'] = index
    order = dca_orders[index]
    text = f'''
*dca Orders*

You currently have {len(dca_orders)} dca orders. You can manage your orders here.

Your orders are:
    '''
    keyboard = get_keyboard(message.chat.id, order, index)
    bot.delete_message(chat_id=message.chat.id,
                       message_id=message.message_id)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def handle_remove_order(bot, message):
    orders = main_api.get_dca_orders(message.chat.id)
    index = current_dca_order['index']
    tx_hash = orders[index]['thread_id']
    main_api.remove_dca_order(message.chat.id, tx_hash)
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
    main_api.update_dca_order(message.chat.id, updat_values)
    bot.send_message(chat_id=message.chat.id,
                     text="Successfully updated order!!!")


def handle_input_value(bot, message, item):
    orders = main_api.get_dca_orders(message.chat.id)
    index = current_dca_order['index']
    order = orders[index]
    updat_values[item] = message.text
    text = f'''
*dca Orders*

You currently have {len(orders)} dca orders. You can manage your orders here.

Your orders are:
    '''
    keyboard = get_keyboard(message.chat.id, updat_values, index)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
