from telebot import types
from src.engine import api as main_api

current_token_sniper = {'index': 0}
updat_values = {'id': 0, 'stage':'buy', 'chain':0, 'token': "", 'amount': 0, 'slippage': 0,'wallet_id': 0, 'auto_sell':[]}

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
        f'Amount: {order['amount']}SOL', callback_data='handle_token_sniper_input amount')

    slippage = types.InlineKeyboardButton(
        f'Slippage: {order['slippage']}%', callback_data='handle_token_sniper_input slippage')

    auto_amount_title = types.InlineKeyboardButton(
        'Amount:', callback_data='2')
    auto_price_title = types.InlineKeyboardButton(
        'Price:', callback_data='2')
    auto_add_button = types.InlineKeyboardButton(
        'Add', callback_data='handle_sniper_add_auto_param')


    auto_amounts = []
    for index in range(len(order['auto_sell'])):
      auto_amount_x = types.InlineKeyboardButton(
          text=f'''{order['auto_sell'][index]['amount']}%''', callback_data=f'handle_sniper_auto_amount {index}')
      auto_amounts.append(auto_amount_x)

    auto_prices = []
    for index in range(len(order['auto_sell'])):
      auto_price_x = types.InlineKeyboardButton(
          text=f'''{order['auto_sell'][index]['price']}X''', callback_data=f'handle_sniper_auto_price {index}')
      auto_prices.append(auto_price_x)

    auto_removes = []
    for index in range(len(order['auto_sell'])):
      auto_remove_x = types.InlineKeyboardButton(
          text='remove', callback_data=f'handle_sniper_remove_auto_params {index}')
      auto_removes.append(auto_remove_x)
    
    auto_sell = types.InlineKeyboardButton(
        'Auto Sell', callback_data='333')
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
    keyboard.row(token)
    keyboard.row(wallet, amount, slippage)
    keyboard.row(auto_sell)
    for index in range(len(order['auto_sell'])):
      keyboard.row(auto_amount_title, auto_amounts[index], auto_price_title, auto_prices[index], auto_removes[index])
    keyboard.row(auto_add_button)
    
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
        print(order)
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

    keyboard = get_keyboard(message.chat.id, order, index)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def handle_prev_order(bot, message):
    token_snipers = main_api.get_token_snipers(message.chat.id)
    index = current_token_sniper['index']
    index -= 1
    current_token_sniper['index'] = index
    order = token_snipers[index]
    keyboard = get_keyboard(message.chat.id, order, index)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_remove_order(bot, message):
    orders = main_api.get_token_snipers(message.chat.id)
    index = current_token_sniper['index']
    removal_id = orders[index]['id']
    main_api.remove_token_sniper(message.chat.id, removal_id)
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

def handle_input_auto_amount(bot, message, item):
    text = '''
*Update Order*
Enter the value to change:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_auto_amount_value(bot, next_message, item))
  
def handle_input_auto_price(bot, message, item):
    text = '''
*Update Order*
Enter the value to change:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_auto_price_value(bot, next_message, item))

def handle_input_auto_price_value(bot, message, item):
    orders = main_api.get_token_snipers(message.chat.id)
    index = current_token_sniper['index']
    order = orders[index]
    updat_values['auto_sell'][int(item)]['price'] = message.text
    text = f'''
*Token Snipers*

You currently have {len(orders)} Token Snipers. You can manage your orders here.

Your orders are:
    '''
    keyboard = get_keyboard(message.chat.id, updat_values, index)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def handle_input_auto_amount_value(bot, message, item):
    orders = main_api.get_token_snipers(message.chat.id)
    index = current_token_sniper['index']
    order = orders[index]
    updat_values['auto_sell'][int(item)]['amount'] = message.text
    text = f'''
*Token Snipers*

You currently have {len(orders)} Token Snipers. You can manage your orders here.

Your orders are:
    '''
    keyboard = get_keyboard(message.chat.id, updat_values, index)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def handle_remove_auto_param(bot, message, item):
    orders = main_api.get_token_snipers(message.chat.id)
    index = current_token_sniper['index']
    order = orders[index]
    id = int(item)
    
    updat_values['auto_sell'].pop(id)
    text = f'''
*Token Snipers*

You currently have {len(orders)} Token Snipers. You can manage your orders here.

Your orders are:
    '''
    keyboard = get_keyboard(message.chat.id, updat_values, index)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_add_auto_param(bot, message):
    orders = main_api.get_token_snipers(message.chat.id)
    index = current_token_sniper['index']
    order = orders[index]
    new_param = {'amount':0, 'price':0}
    updat_values['auto_sell'].append(new_param)
    text = f'''
*Token Snipers*

You currently have {len(orders)} Token Snipers. You can manage your orders here.

Your orders are:
    '''
    keyboard = get_keyboard(message.chat.id, updat_values, index)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
    
def handle_update_order(bot, message):
    index = current_token_sniper['index']
    orders = main_api.get_token_snipers(message.chat.id)
    update_id = orders[index]['id']
    print(update_id)
    chain_index = main_api.get_chain(message.chat.id)
    updat_values['chain'] = chain_index
    main_api.set_token_sniper(message.chat.id, update_id, updat_values)
    bot.send_message(chat_id=message.chat.id,
                     text="Successfully updated order!!!")


def handle_input_value(bot, message, item):
    orders = main_api.get_token_snipers(message.chat.id)
    index = current_token_sniper['index']
    order = orders[index]
    updat_values[item] = message.text
    text = f'''
*Token Snipers*

You currently have {len(orders)} token snipers. You can manage your snipers here.

Your snipers are:
    '''
    keyboard = get_keyboard(message.chat.id, updat_values, index)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
