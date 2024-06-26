from telebot import types
from src.engine import api as main_api

current_limit_order = {'index': 0}
updat_values = {'id':0, 'chain':0, 'type': 0, 'token': "", 'amount': 0, 'slippage':0,'wallet_id': 0,'market_capital': 0}


def get_keyboard(chat_id, order, order_index):
    keyboard = types.InlineKeyboardMarkup()
    updat_values.update(order)
    
    token_symbol = main_api.get_token_metadata(chat_id, order['token'])['symbol']
    wallets = main_api.get_wallets(chat_id)
    for index in range(len(wallets)):
      if wallets[index]['id'] == order['wallet_id']:
        wallet_index = index
    index_button = types.InlineKeyboardButton(
        f'Order: {order_index + 1}', callback_data='aaa')
    type = types.InlineKeyboardButton(
        f'Type: {order['type']}', callback_data='aaa')
    token = types.InlineKeyboardButton(
        f'Token: {token_symbol}', callback_data='aaa')
    wallet = types.InlineKeyboardButton(
        f'Wallet: W{wallet_index+1}', callback_data='aaa')
    amount = types.InlineKeyboardButton(
        f'Amount: {order['amount']}SOL', callback_data='handle_limit_input amount')
    limit_token_price = types.InlineKeyboardButton(
        f'Market Cap: {order['market_capital']}', callback_data='handle_limit_input market_capital')
    slippage = types.InlineKeyboardButton(
        f'Slippage: {order['slippage']}%', callback_data='handle_limit_input slippage')
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
    keyboard.row(token)
    keyboard.row(type, amount, wallet)
    keyboard.row(limit_token_price, slippage)
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
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


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
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def handle_remove_order(bot, message):
    orders = main_api.get_limit_orders(message.chat.id)
    index = current_limit_order['index']
    remove_id = orders[index]['id']
    main_api.remove_limit_order(message.chat.id, remove_id)
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
    index = current_limit_order['index']
    orders = main_api.get_limit_orders(message.chat.id)
    update_id = orders[index]['id']
    print(update_id)
    chain_index = main_api.get_chain(message.chat.id)
    updat_values['chain'] = chain_index
    main_api.set_limit_order(message.chat.id, update_id, updat_values)
    bot.send_message(chat_id=message.chat.id,
                     text="Successfully updated order!!!")


def handle_input_value(bot, message, item):
    orders = main_api.get_limit_orders(message.chat.id)
    index = current_limit_order['index']
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
