from telebot import types
from src.engine import api as main_api
import threading
import time

current_pending_order = {'index': 0}


def get_keyboard(chat_id, order, order_index):
    orders = main_api.get_pending_orders(chat_id)
    keyboard = types.InlineKeyboardMarkup()
    index_button = types.InlineKeyboardButton(
        f'Order: {order_index + 1}', callback_data='aaa')
    if order['type'] == 0:
        caption = 'Type: Buy'
    else:
        caption = 'Type: Sell'
    type = types.InlineKeyboardButton(caption, callback_data='aaa')
    token = types.InlineKeyboardButton(
        f'Token: {order['token']}', callback_data='aaa')
    tx_hash = types.InlineKeyboardButton(
        f'Token: {order['tx_hash']}', callback_data='aaa')
    wallet = types.InlineKeyboardButton(
        f'Wallet: W{order['wallet']}', callback_data='aaa')
    amount = types.InlineKeyboardButton(
        f'Buy Amount: {order['buy_amount']}E', callback_data='aaa')
    gas_amount = types.InlineKeyboardButton(
        f'Gas Amount: {order['gas_amount']}', callback_data='aaa')
    gas_price = types.InlineKeyboardButton(
        f'Gas Price: {order['gas_price']}', callback_data='aaa')
    slippage = types.InlineKeyboardButton(
        f'Slippage: {order['slippage']}%', callback_data='aaa')
    left_button = types.InlineKeyboardButton(
        '<<', callback_data='handle_prev_pending_order')
    right_button = types.InlineKeyboardButton(
        '>>', callback_data='handle_next_pending_order')
    update = types.InlineKeyboardButton('Update', callback_data='aaa')
    cancel = types.InlineKeyboardButton(
        'Cancel Order', callback_data='handle_remove_pending_order')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')

    keyboard.row(left_button, index_button, right_button)
    keyboard.row(type, token)
    keyboard.row(wallet, amount)
    keyboard.row(gas_amount, gas_price, slippage)
    keyboard.row(update, cancel)
    keyboard.row(back, close)
    return keyboard


def handle_orders(bot, message):
    pending_orders = main_api.get_pending_orders(message.chat.id)
    text = f'''
*Pending Orders*

You currently have {len(pending_orders)} pending orders. You can manage your orders here.

Your orders are:
    '''

    if len(pending_orders) == 0:
        bot.send_message(chat_id=message.chat.id,
                         text='You have no pending orders')
    else:
        order = pending_orders[current_pending_order['index']]

        keyboard = get_keyboard(
            message.chat.id, order, current_pending_order['index'])
        bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                         reply_markup=keyboard, disable_web_page_preview=True)


def handle_next_order(bot, message):
    index = current_pending_order['index']
    index += 1
    current_pending_order['index'] = index
    pending_orders = main_api.get_pending_orders(message.chat.id)
    order = pending_orders[index]
    text = f'''
*Pending Orders*

You currently have {len(pending_orders)} pending orders. You can manage your orders here.

Your orders are:
    '''
    keyboard = get_keyboard(message.chat.id, order, index)
    bot.delete_message(chat_id=message.chat.id,
                       message_id=message.message_id)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def handle_prev_order(bot, message):

    pending_orders = main_api.get_pending_orders(message.chat.id)
    index = current_pending_order['index']
    index -= 1
    current_pending_order['index'] = index
    order = pending_orders[index]
    text = f'''
*Pending Orders*

You currently have {len(pending_orders)} pending orders. You can manage your orders here.

Your orders are:
    '''
    keyboard = get_keyboard(message.chat.id, order, index)
    bot.delete_message(chat_id=message.chat.id,
                       message_id=message.message_id)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def handle_remove_order(bot, message):
    orders = main_api.get_pending_orders(message.chat.id)
    index = current_pending_order['index']
    tx_hash = orders[index]['tx_hash']
    main_api.remove_pending_order(message.chat.id, tx_hash)
    bot.send_message(chat_id=message.chat.id,
                     text="Successfully cancelled order!!!")
    handle_orders(bot, message)
