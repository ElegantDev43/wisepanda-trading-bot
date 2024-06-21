from telebot import types

# import config
from src.engine import api as main_api

auto_keyboard = {'buy':{'status':0,'amount':0, 'slippage':0, 'stop_loss':0},
                 'sell':{'status':0,'amount':0, 'slippage':0}}

def get_keyboard(current_keyboard):
    auto_keyboard.update(current_keyboard)
    keyboard = types.InlineKeyboardMarkup()
    auto_buy = types.InlineKeyboardButton(
        text='Auto Buy:', callback_data='333')
    auto_sell = types.InlineKeyboardButton(
        text='Auto Sell:', callback_data='333')
    amount_title = types.InlineKeyboardButton(
        text='Amount:', callback_data='333')
    slippage_title = types.InlineKeyboardButton(
        text='Slippage:', callback_data='333')
    stop_loss_title = types.InlineKeyboardButton(
        text='Stop Loss:', callback_data='333')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='settings')

    buy_amount = types.InlineKeyboardButton(
        text=f'{current_keyboard['buy']['amount']}', callback_data='handle_input_auto_buy_order amount')
    buy_slippage = types.InlineKeyboardButton(
        text=f'{current_keyboard['buy']['slippage']}%', callback_data='handle_input_auto_buy_order slippage')
    buy_stop_loss = types.InlineKeyboardButton(
        text=f'{current_keyboard['buy']['stop_loss']}%', callback_data='handle_input_auto_buy_order stop_loss')

    sell_amount = types.InlineKeyboardButton(
        text=f'{current_keyboard['sell']['amount']}', callback_data='handle_input_auto_sell_order amount')
    sell_slippage = types.InlineKeyboardButton(
        text=f'{current_keyboard['sell']['slippage']}%', callback_data='handle_input_auto_sell_order slippage')
   
    caption1 = ''
    if auto_keyboard['buy']['status'] == 1:
      caption1 = '🟢 Enabled'
    elif auto_keyboard['buy']['status'] == 0:
      caption1 = '🔴 Disabled'
    enable_auto_buy = types.InlineKeyboardButton(
        text=caption1, callback_data='auto_buy_order_status_change')

    caption2 = ''
    if auto_keyboard['sell']['status'] == 1:
      caption2 = '🟢 Enabled'
    elif auto_keyboard['sell']['status'] == 0:
      caption2 = '🔴 Disabled'
    enable_auto_sell = types.InlineKeyboardButton(
        text=caption2, callback_data='auto_sell_order_status_change')
    
    update_btn = types.InlineKeyboardButton(
        text="Update", callback_data='handle update auto order')
    keyboard.row(auto_buy, enable_auto_buy)
    keyboard.row(amount_title, buy_amount, slippage_title, buy_slippage, stop_loss_title, buy_stop_loss)

    keyboard.row(auto_sell, enable_auto_sell)
    keyboard.row(amount_title, sell_amount, slippage_title, sell_slippage)
    keyboard.row(update_btn, back)
    return keyboard

def handle_auto_orders(bot, message):
    text = '''
    *Settings > Auto Order 🎮*
    
    You can set default criterias for auto trading of our bot..
    '''
    value_keyboard = main_api.get_auto_order(message.chat.id)
    keyboard = get_keyboard(value_keyboard)

    bot.send_message(chat_id=message.chat.id, text=text,
                     parse_mode='Markdown', reply_markup=keyboard)

def handle_buy_input(bot, message, item):
    text = '''
*Update Key*
Enter the value to change:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_buy_input_value(bot, next_message, item))
    

def handle_buy_input_value(bot, message, item):
    
    auto_keyboard['buy'][item] = message.text
    text = '''
    *Settings > Auto Order 🎮*
    
    You can set default criterias for auto trading of our bot..
    '''
    keyboard = get_keyboard(auto_keyboard)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def handle_sell_input(bot, message, item):
    text = '''
*Update Key*
Enter the value to change:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_sell_input_value(bot, next_message, item))
    

def handle_sell_input_value(bot, message, item):
    
    auto_keyboard['sell'][item] = message.text
    text = '''
    *Settings > Auto Order 🎮*
    
    You can set default criterias for auto trading of our bot..
    '''
    keyboard = get_keyboard(auto_keyboard)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def handle_buy_status(bot, message):
    if auto_keyboard['buy']['status'] == 0:
      auto_keyboard['buy']['status'] = 1
    elif auto_keyboard['buy']['status'] == 1:
      auto_keyboard['buy']['status'] = 0
    text = '''
    *Settings > Auto Order 🎮*
    
    You can set default criterias for auto trading of our bot..
    '''
    keyboard = get_keyboard(auto_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
    
def handle_sell_status(bot, message):
    if auto_keyboard['sell']['status'] == 0:
      auto_keyboard['sell']['status'] = 1
    elif auto_keyboard['sell']['status'] == 1:
      auto_keyboard['sell']['status'] = 0
    text = '''
    *Settings > Auto Order 🎮*
    
    You can set default criterias for auto trading of our bot..
    '''
    keyboard = get_keyboard(auto_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
     
def handle_update(bot, message):
    print(auto_keyboard)
    main_api.set_auto_order(message.chat.id, auto_keyboard)