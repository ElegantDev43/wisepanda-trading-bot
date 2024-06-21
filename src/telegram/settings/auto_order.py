from telebot import types

# import config
from src.engine import api as main_api

auto_keyboard = {'status':0,'amount':0, 'slippage':0}

def get_keyboard(current_keyboard):
    keyboard = types.InlineKeyboardMarkup()
    amount_title = types.InlineKeyboardButton(
        text='💰Amount:', callback_data='333')
    slippage_title = types.InlineKeyboardButton(
        text='💧Slippage:', callback_data='333')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='settings')

    amount = types.InlineKeyboardButton(
        text=f'{current_keyboard['amount']}', callback_data='handle_input_auto_order amount')
    slippage = types.InlineKeyboardButton(
        text=f'{current_keyboard['slippage']}', callback_data='handle_input_auto_order slippage')
    caption = ''
    if auto_keyboard['status'] == 1:
      caption = '🟢 Enabled'
    elif auto_keyboard['status'] == 0:
      caption = '🔴 Disabled'
    enable_order = types.InlineKeyboardButton(
        text=caption, callback_data='aut_order_status_change')

    update_btn = types.InlineKeyboardButton(
        text="Update", callback_data='handle update auto order')
    
    keyboard.row(amount_title, amount, slippage_title, slippage)
    keyboard.row(enable_order, update_btn)
    keyboard.row(back)
    return keyboard

def handle_auto_orders(bot, message):
    text = '''
    *Settings > Auto Order 🎮*
    
    You can set criterias for auto order here.
    '''
    value_keyboard = main_api.get_auto_order(message.chat.id)
    keyboard = get_keyboard(value_keyboard)

    bot.send_message(chat_id=message.chat.id, text=text,
                     parse_mode='Markdown', reply_markup=keyboard)

def handle_input(bot, message, item):
    text = '''
*Update Key*
Enter the value to change:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))
    

def handle_input_value(bot, message, item):
    
    auto_keyboard[item] = message.text
    text = '''
    *Settings > Auto Order 🎮*
    
    You can set criterias for auto order here.
    '''
    keyboard = get_keyboard(auto_keyboard)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def handle_status(bot, message):
    if auto_keyboard['status'] == 0:
      auto_keyboard['status'] = 1
    elif auto_keyboard['status'] == 1:
      auto_keyboard['status'] = 0
    text = '''
    *Settings > Auto Order 🎮*
    
    You can set criterias for auto order here.
    '''
    keyboard = get_keyboard(auto_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
    
def handle_update(bot, message):
    print(auto_keyboard)
    main_api.set_auto_order(message.chat.id, auto_keyboard)