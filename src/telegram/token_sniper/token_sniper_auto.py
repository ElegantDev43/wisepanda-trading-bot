from telebot import types

from src.telegram import user_manage as feature_api
from src.engine import api as main_api

current_keyboard = {}
auto_sell_status = {'status':0}
def handle_start(bot, message):
    text = '''
 *🎯 Token Sniper* >> Auto Mode

Set your parameters for auto token snipping.
    '''
    feature_api.initialize_values(message.chat.id, 'token_sniper_auto')
    keyboard_data = feature_api.get_user_feature_values(message.chat.id, 'token_sniper_auto')
    current_keyboard.update(keyboard_data)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    #print(current_keyboard)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def get_keyboard(chat_id, keyboard_data):
    keyboard = types.InlineKeyboardMarkup()
    wallets = []
    chain_wallets = main_api.get_wallets(chat_id)
    wallet_count = len(chain_wallets)
    for index in range(wallet_count):
        caption = f'{"🟢" if index == keyboard_data['wallet'] else ""} W{
            index + 1}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"token_sniper_auto select buy wallet {index}")
        wallets.append(button)
    more_wallet_btn = types.InlineKeyboardButton('🔽', callback_data='token_sniper_auto show more wallets')


    amount_title = types.InlineKeyboardButton(
        'Amount:', callback_data='set title')
    buy_amount = types.InlineKeyboardButton(
        text="🟢 1 SOL" if keyboard_data['amount'] == 10**9 else "1 SOL", callback_data='token_sniper_auto amount default')
    if keyboard_data['amount'] == -999:
      caption = 'X SOL ✏️'
    elif keyboard_data['amount'] == 10**9:
      caption = 'X SOL ✏️'
    else:
      caption = f'''🟢 {int(keyboard_data['amount'] / (10 ** 9))} SOL'''
    buy_amount_x = types.InlineKeyboardButton(
        text=caption, callback_data='token_sniper_auto amount x')

    slippage = types.InlineKeyboardButton(
        text="🟢 Auto Slippage" if keyboard_data['slippage'] == 50 else "Auto Slippage", callback_data='token_sniper_auto slippage default')
    if keyboard_data['slippage'] == -999:
      caption = 'X Slippage ✏️'
    elif keyboard_data['slippage'] == 50:
      caption = 'X Slippage ✏️'
    else:
      caption = f'''🟢 {keyboard_data['slippage']}% Slippage'''
    slippage_x = types.InlineKeyboardButton(
        text=caption, callback_data='token_sniper_auto slippage x')
    
    if keyboard_data['stop-loss'] == 0:
      caption = "✏️ Stop Loss:"
    else:
      caption = f"✏️ Stop Loss: {keyboard_data['stop-loss']}%"
    stop_loss_x = types.InlineKeyboardButton(
          text=caption, callback_data='token_sniper_auto stop-loss')

    if keyboard_data['min_market_cap'] == 0:
      caption = "✏️ Min MarketCap: _"
    else:
      caption = f"✏️ Min MarketCap: {keyboard_data['min_market_cap']}"
    min_market_cap = types.InlineKeyboardButton(
          text=caption, callback_data='token_sniper_auto min_market_cap')
    
    if keyboard_data['max_market_cap'] == 0:
      caption = "✏️ Max MarketCap: _"
    else:
      caption = f"✏️ Max MarketCap: {keyboard_data['max_market_cap']}"
    max_market_cap = types.InlineKeyboardButton(
          text=caption, callback_data='token_sniper_auto max_market_cap')
    
    auto_sell = types.InlineKeyboardButton(
        '🔻 Set Auto Sell', callback_data='token_sniper_auto set auto_sell')

    auto_add_button = types.InlineKeyboardButton(
        'Add Sell Stage', callback_data='token_sniper_auto add auto params')
    auto_remove_button = types.InlineKeyboardButton(
        'Remove Sell Stage', callback_data='token_sniper_auto remove auto params')

    if main_api.get_auto_sniper(chat_id)['token']['active'] ==  True:
      caption = "Stop Sniper"
    else:
      caption = "Start Sniper"
    create_order = types.InlineKeyboardButton(text=caption, callback_data='make sniper auto order')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')

    if keyboard_data['wallet_row'] == 1:
      keyboard.row(*wallets[4*(keyboard_data['wallet_row']-1): 4*(keyboard_data['wallet_row']-1) + 3], more_wallet_btn)
    else:
      for index in range(keyboard_data['wallet_row'] - 1):
        keyboard.row(*wallets[4*index: 4 * index + 4])
      last_index = keyboard_data['wallet_row'] -1
      if 4 * (last_index + 1) <= wallet_count:
        keyboard.row(*wallets[4 * last_index: 4 * last_index + 3], more_wallet_btn)
      else:
        keyboard.row(*wallets[4 * last_index: wallet_count])



    keyboard.row(buy_amount, buy_amount_x)
    keyboard.row(slippage, slippage_x)
    keyboard.row(min_market_cap, max_market_cap)
    keyboard.row(stop_loss_x)
    keyboard.row(auto_sell)
    if auto_sell_status['status'] == 1:
      keyboard.row(auto_add_button, auto_remove_button)
      for index in range(len(keyboard_data['chain_auto_sell_params'])):
        auto_amount = types.InlineKeyboardButton(
          f'✏️ Sell Amount(%): {keyboard_data['chain_auto_sell_params'][index]['amount']}%' if keyboard_data['chain_auto_sell_params'][index]['amount'] != 0 else '✏️ Sell Amount(%): _', callback_data=f'token_sniper_auto auto_sell {index}')
        auto_profit = types.InlineKeyboardButton(
          f'✏️ Sell Profit: {keyboard_data['chain_auto_sell_params'][index]['profit']}x' if keyboard_data['chain_auto_sell_params'][index]['profit'] != 0 else '✏️ Sell Profit: _', callback_data=f'token_sniper_auto auto_profit {index}')
        keyboard.row(auto_amount, auto_profit)
    keyboard.row(create_order)
    keyboard.row(back, close)

    return keyboard


def handle_default_values(bot, message, item):
    current_keyboard[item] = 10**9
    #print(current_keyboard)
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_auto', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
    
def handle_x_values(bot, message, item):
    text = f'''
*🎯 Token Sniper* >> Auto Mode
Enter the {item} to set:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))
    
def handle_input_value(bot, message, item):
    if item == 'amount':
      current_keyboard[item] = float(message.text) * 10 ** 9
    elif item == 'slippage':
      current_keyboard[item] = int(message.text)
    elif item == 'stop-loss':
      current_keyboard[item] = int(message.text)
    #print(current_keyboard)
    else:
      current_keyboard[item] = int(message.text)
    text = '''
 *🎯 Token Sniper* >> Auto Mode

Set your parameters for auto token snipping.
    '''
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_auto', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def handle_confirm_auto_slippage(bot, message):
  text = '''
      *🎯 Token Sniper* >> Auto Mode
 Do you confirm maximum of 50% slippage as Auto Slippage?.
'''
  keyboard = types.InlineKeyboardMarkup()
  cancel = types.InlineKeyboardButton('Cancel', callback_data='token_sniper_auto slippage x')
  confirm = types.InlineKeyboardButton('Confirm', callback_data=f'token_sniper_auto slippage confirm')
  keyboard.row(cancel, confirm)
  bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                    reply_markup=keyboard, disable_web_page_preview=True)
  
def handle_default_slippage(bot, message):
    current_keyboard['slippage'] = 50
    text = '''
 *🎯 Token Sniper* >> Auto Mode

Set your parameters for auto token snipping.
    '''
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_auto', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def select_wallet(bot, message, index):
    current_keyboard['wallet'] = int(index)
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_auto', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
    
def handle_show_more_wallets(bot, message):
    current_keyboard['wallet_row'] += 1
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_auto', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
    
def handle_auto_sell_status(bot, message):
    if auto_sell_status['status'] == 0:
      auto_sell_status['status'] = 1
    elif auto_sell_status['status'] == 1:
      auto_sell_status['status'] = 0
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_add_auto_sell_param(bot, message):
    new_param = {'amount':0, 'profit':0}
    current_keyboard['chain_auto_sell_params'].append(new_param)
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_auto', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_remove_auto_sell_param(bot, message):
    length = len(current_keyboard['chain_auto_sell_params'])
    current_keyboard['chain_auto_sell_params'].pop(length-1)
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_auto', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
    
def handle_auto_sell_input_values(bot, message, index):
    text = f'''
*🎯 Token Sniper* >> Auto Mode
Enter the amount to sell:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_auto_sell_inputs(bot, next_message, int(index)))
    
def handle_auto_sell_inputs(bot, message, index):
    current_keyboard['chain_auto_sell_params'][index]['amount'] = int(message.text)
    text = '''
 *🎯 Token Sniper* >> Auto Mode

Set your parameters for auto token snipping.
    '''
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_auto', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def handle_auto_profit_input_values(bot, message, index):
    text = f'''
*🎯 Token Sniper* >> Auto Mode
Enter the profit to get in sell:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_auto_profit_inputs(bot, next_message, int(index)))
    
def handle_auto_profit_inputs(bot, message, index):
    current_keyboard['chain_auto_sell_params'][index]['profit'] = int(message.text)
    text = '''
 *🎯 Token Sniper* >> Auto Mode

Set your parameters for auto token snipping.
    '''
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_auto', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
    
def handle_sniper_status(bot, message):
  wallets = main_api.get_wallets(message.chat.id)
  buy_wallet = wallets[current_keyboard['wallet']]['id']
  auto_sniper = main_api.get_auto_sniper(message.chat.id)
  if auto_sniper['token']['active'] == True:
      auto_sniper['token']['active'] = False
      bot.send_message(chat_id=message.chat.id,
                     text='Successfully stopped Sniper')
  elif auto_sniper['token']['active'] == False:
      buy_amount = int(current_keyboard['amount'])
      auto_sniper = {
        'token': {
          'active': True,
          'amount': buy_amount,
          'slippage': int(current_keyboard['slippage']),
          'wallet_id':  buy_wallet,
          'auto_sell': current_keyboard['chain_auto_sell_params'],
          'min_market_capital': int(current_keyboard['min_market_cap']),
          'max_market_capital': int(current_keyboard['max_market_cap']),
          'stop_loss':int(current_keyboard['stop-loss'])
        },
        'lp': {
          'active': False,
          'amount': 1,
          'slippage': 50,
          'wallet_id': 0
        }
      }
      main_api.set_auto_sniper(message.chat.id, auto_sniper)
      bot.send_message(chat_id=message.chat.id,
                     text='Successfully Started Sniper')
  keyboard = get_keyboard(message.chat.id, current_keyboard)
  bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)