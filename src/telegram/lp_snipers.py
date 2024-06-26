from telebot import types
from src.engine import api as main_api

current_token_sniper = {'index': 0}
updat_values = {'id': 0, 'stage':'buy', 'chain':0, 'token': "", 'amount': 0, 'slippage': 0,'wallet_id': 0}

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
    token = types.InlineKeyboardButton(
        f'Token: {token_symbol}', callback_data='aaa')
    wallet = types.InlineKeyboardButton(
        f'Wallet: W{wallet_index+1}', callback_data='aaa')
    amount = types.InlineKeyboardButton(
        f'Amount: {order['amount']}SOL', callback_data='handle_lp_sniper_input amount')

    slippage = types.InlineKeyboardButton(
        f'Slippage: {order['slippage']}%', callback_data='handle_lp_sniper_input slippage')

    left_button = types.InlineKeyboardButton(
        '<<', callback_data='handle_prev_lp_sniper')
    right_button = types.InlineKeyboardButton(
        '>>', callback_data='handle_next_lp_sniper')
    update = types.InlineKeyboardButton(
        'Update', callback_data='handle_update_lp_sniper')
    cancel = types.InlineKeyboardButton(
        'Cancel Order', callback_data='handle_remove_lp_sniper')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')

    keyboard.row(left_button, index_button, right_button)
    keyboard.row(token, wallet)
    keyboard.row(amount, slippage)
    keyboard.row(update, cancel)
    keyboard.row(back, close)
    return keyboard


def handle_orders(bot, message):
    token_snipers = main_api.get_lp_snipers(message.chat.id)
    text = f'''
*LP Snipers*

You currently have {len(token_snipers)} snipers. You can manage your snipers here.

Your snipers are:
    '''
    if len(token_snipers) == 0:
        bot.send_message(chat_id=message.chat.id, text='You have no snipers')
    else:
        order = token_snipers[current_token_sniper['index']]
        print(order)
        keyboard = get_keyboard(message.chat.id, order,
                                current_token_sniper['index'])
        bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                         reply_markup=keyboard, disable_web_page_preview=True)


def handle_next_order(bot, message):
    index = current_token_sniper['index']
    index += 1
    current_token_sniper['index'] = index
    token_snipers = main_api.get_lp_snipers(message.chat.id)

    order = token_snipers[index]

    keyboard = get_keyboard(message.chat.id, order, index)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def handle_prev_order(bot, message):
    token_snipers = main_api.get_lp_snipers(message.chat.id)
    index = current_token_sniper['index']
    index -= 1
    current_token_sniper['index'] = index
    order = token_snipers[index]
    keyboard = get_keyboard(message.chat.id, order, index)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_remove_order(bot, message):
    orders = main_api.get_lp_snipers(message.chat.id)
    index = current_token_sniper['index']
    removal_id = orders[index]['id']
    main_api.remove_lp_sniper(message.chat.id, removal_id)
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
    index = current_token_sniper['index']
    orders = main_api.get_lp_snipers(message.chat.id)
    update_id = orders[index]['id']
    print(update_id)
    chain_index = main_api.get_chain(message.chat.id)
    updat_values['chain'] = chain_index
    main_api.set_lp_sniper(message.chat.id, update_id, updat_values)
    bot.send_message(chat_id=message.chat.id,
                     text="Successfully updated order!!!")


def handle_input_value(bot, message, item):
    orders = main_api.get_lp_snipers(message.chat.id)
    index = current_token_sniper['index']
    order = orders[index]
    updat_values[item] = message.text
    text = f'''
*LP Snipers*

You currently have {len(orders)} LP Snipers. You can manage your snipers here.

Your snipers are:
    '''
    keyboard = get_keyboard(message.chat.id, updat_values, index)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
