from telebot import types

from src.engine import api as main_api
from src.telegram import user_manage as feature_api
from src.engine.swing import api as swing_api

current_keyboard = {}


def handle_start(bot, message):
   # user_model.create_user_by_telegram(message.chat.id)
    text = '''
*🪁 Swing Trading* >> Auto Mode

Automatically perform swing trading.
    '''
    feature_api.initialize_values(message.chat.id, 'swing_auto')
    keyboard_data = feature_api.get_user_feature_values(message.chat.id, 'swing_auto')
    current_keyboard.update(keyboard_data)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
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
            text=caption, callback_data=f"swing_auto select buy wallet {index}")
        wallets.append(button)
    more_wallet_btn = types.InlineKeyboardButton('🔽', callback_data='swing_auto show more wallets')

    buy_amount = types.InlineKeyboardButton(
        text="🟢 1 SOL" if keyboard_data['amount'] == 10**9 else "1 SOL", callback_data='swing_auto amount default')
    if keyboard_data['amount'] == -999:
      caption = 'X SOL ✏️'
    elif keyboard_data['amount'] == 10**9:
      caption = 'X SOL ✏️'
    else:
      caption = f'''🟢 {float(keyboard_data['amount'] / (10 ** 9))} SOL'''
    buy_amount_x = types.InlineKeyboardButton(
        text=caption, callback_data='swing_auto amount x')

    slippage = types.InlineKeyboardButton(
        text="🟢 Auto Slippage" if keyboard_data['slippage'] == 50 else "Auto Slippage", callback_data='swing_auto slippage default')
    if keyboard_data['slippage'] == -999:
      caption = 'X Slippage ✏️'
    elif keyboard_data['slippage'] == 50:
      caption = 'X Slippage ✏️'
    else:
      caption = f'''🟢 {keyboard_data['slippage']}% Slippage'''
    slippage_x = types.InlineKeyboardButton(
        text=caption, callback_data='swing_auto slippage x')

    if keyboard_data['market_capital'] == 0:
      caption = "✏️ Market Capital: _"
    else:
      caption = f"✏️ Market Capital: {keyboard_data['market_capital']}"
    max_market_cap = types.InlineKeyboardButton(
          text=caption, callback_data='swing_auto market_capital')


    if keyboard_data['stop-loss'] == 0:
      caption = "✏️ Stop Loss: _"
    else:
      caption = f"✏️ Stop Loss: {keyboard_data['stop-loss']}%"
    stop_loss_x = types.InlineKeyboardButton(
          text=caption, callback_data='swing_auto stop-loss')

    if keyboard_data['take-profit'] == 0:
      caption = "✏️ Take Profit: _"
    else:
      caption = f"✏️ Take Profit: {keyboard_data['take-profit']}%"
    take_profit = types.InlineKeyboardButton(
          text=caption, callback_data='swing_auto take-profit')


    if main_api.get_auto_swing_status(chat_id) == 0:
      caption = 'Start'
    elif main_api.get_auto_swing_status(chat_id) == 1:
      caption = 'Stop'
    create_order = types.InlineKeyboardButton(text = caption, callback_data='swing_auto start trading')
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
    keyboard.row(take_profit, stop_loss_x)
    keyboard.row(max_market_cap)
    keyboard.row(create_order)
    keyboard.row(back, close)

    return keyboard


def handle_default_values(bot, message, item):
    current_keyboard[item] = 10**9
    #print(current_keyboard)
    feature_api.update_user_feature_values(message.chat.id, 'swing_auto', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_x_values(bot, message, item):
    text = f'''
🪁 Swing Trading >> Auto Mode
Enter the {item} to set:
'''
    bot.send_message(chat_id=message.chat.id, text=text)
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
*🪁 Swing Trading* >> Auto Mode

Automatically perform swing trading.
    '''
    feature_api.update_user_feature_values(message.chat.id, 'swing_auto', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def handle_confirm_auto_slippage(bot, message):
  text = '''
      *🪁 Swing Trading* >> Auto Mode
 Do you confirm maximum of 50% slippage as Auto Slippage?.
'''
  keyboard = types.InlineKeyboardMarkup()
  cancel = types.InlineKeyboardButton('Cancel', callback_data='swing_auto slippage x')
  confirm = types.InlineKeyboardButton('Confirm', callback_data=f'swing_auto slippage confirm')
  keyboard.row(cancel, confirm)
  bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                    reply_markup=keyboard, disable_web_page_preview=True)

def handle_default_slippage(bot, message):
    current_keyboard['slippage'] = 50
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    text = '''
*🪁 Swing Trading* >> Auto Mode

Automatically perform swing trading.
    '''
    feature_api.update_user_feature_values(message.chat.id, 'swing_auto', current_keyboard)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def select_wallet(bot, message, index):
    current_keyboard['wallet'] = int(index)
    feature_api.update_user_feature_values(message.chat.id, 'swing_auto', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_show_more_wallets(bot, message):
    current_keyboard['wallet_row'] += 1
    feature_api.update_user_feature_values(message.chat.id, 'swing_auto', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_trading_tatus(bot, message):
    wallets = main_api.get_wallets(message.chat.id)
    buy_wallet = wallets[current_keyboard['wallet']]['id']
    if current_keyboard['amount'] == 0:
        bot.send_message(chat_id=message.chat.id,
                     text='Not enough balance in the wallet')
    else:
      if main_api.get_auto_swing_status(message.chat.id) == 0:
        main_api.set_auto_swing_status(message.chat.id, 1)
        swing_api.SetFullyAutoTokens('Start', message.chat.id, current_keyboard['amount'], buy_wallet, current_keyboard['slippage'],current_keyboard['market_capital'], current_keyboard['take-profit'], current_keyboard['stop-loss'])
      elif main_api.get_auto_swing_status(message.chat.id) == 1:
        main_api.set_auto_swing_status(message.chat.id, 0)
        swing_api.SetFullyAutoTokens('Stop', message.chat.id)
      keyboard = get_keyboard(message.chat.id, current_keyboard)
      bot.edit_message_reply_markup(
          chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)