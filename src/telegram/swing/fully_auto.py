from telebot import types
from src.engine import api as main_api

chain_buy_amounts = [1]

from src.database.swing import Htokens as HTokens_model


x_value_list = {"buy-amount": 0, 'more_btn_index':1}

index_list = {'wallet': 100, 'buy_amount': 100}

result = {'wallet': 0, 'buy_amount': 0, 'status':0}

def get_keyboard(update_data, chat_id, index_data):

    keyboard = types.InlineKeyboardMarkup()

    wallets = []

    chain_wallets = main_api.get_wallets(chat_id)
    wallet_count = len(chain_wallets)
    for index in range(wallet_count):
        caption = f'{"🟢" if index == index_data['wallet'] else ""} W{
            index + 1}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"fully_auto swing select buy wallet {index}")
        wallets.append(button)
    more_wallet_btn = types.InlineKeyboardButton('🔽', callback_data='swing auto show more wallets')
    buys = []
    buy_count = len(chain_buy_amounts)
    amount_title = types.InlineKeyboardButton(
        'Amount:', callback_data='set title')
    for index in range(buy_count):
        if index_data['buy_amount'] == 100:
            caption = f'{chain_buy_amounts[index]} SOL'
        else:
            caption = f'{"🟢" if index == index_data['buy_amount'] else ""} {
                chain_buy_amounts[index]} SOL'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"fully_auto swing select buy amount {index}")
        buys.append(button)

    if result['status'] == 0:
      status_caption = 'Start'
    else:
      status_caption = 'Stop'
    status_btn = types.InlineKeyboardButton(text=status_caption, callback_data='handle swing auto mode status')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='swing')
    if update_data['buy-amount'] == 0:
        caption = "X SOL"
    else:
        caption = f"🟢 {update_data['buy-amount']} SOL"
    buy_x = types.InlineKeyboardButton(
        text=caption, callback_data='fully_auto swing select buy amount x')
    
    if update_data['more_btn_index'] == 1:
      keyboard.row(*wallets[4*(update_data['more_btn_index']-1): 4*(update_data['more_btn_index']-1) + 3], more_wallet_btn)
    else:
      for index in range(update_data['more_btn_index'] - 1):
        keyboard.row(*wallets[4*index: 4 * index + 4])
      last_index = update_data['more_btn_index'] -1
      if 4 * (last_index + 1) <= wallet_count:
        keyboard.row(*wallets[4 * last_index: 4 * last_index + 3], more_wallet_btn)
      else:
        keyboard.row(*wallets[4 * last_index: wallet_count])
        
    keyboard.row(amount_title, *buys[0:buy_count], buy_x)
    keyboard.row(status_btn)
    keyboard.row(back)
    return keyboard

def handle_more_btn(bot, message):
    x_value_list['more_btn_index'] += 1
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_start(bot, message):

    text = '''
*🪁 Swing Trading* >> Auto Mode
Select Criterias for Auto Trading.
    '''
    x_value_list['more_btn_index'] = 1
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    #bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def select_buy_wallet(bot, message, index):
   # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]'
    index_list['wallet'] = int(index)
    result['wallet'] = int(index)

    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def select_buy_amount(bot, message, index):
   # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    index_list['buy_amount'] = int(index)
    result['buy_amount'] = chain_buy_amounts[int(index)]
    x_value_list['buy-amount'] = 0


    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
    
def handle_buy_amount_x(bot, message):
    text = '''
*Swing Trading(Auto Mode) > 💰 X*
Enter the amount to set:
'''
    item = "Buy Amount"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))
    
def handle_input_value(bot, message, item):
    bot.delete_message(chat_id=message.chat.id,
                       message_id=message.message_id)
    if item == "Buy Amount":
        buy_amount_x = float(message.text)
        x_value_list['buy-amount'] = buy_amount_x
        result['buy_amount'] = buy_amount_x
        index_list['buy_amount'] = 100
        
    text = '''
*🪁 Swing Trading* >> Auto Mode
Select Criterias for Auto Trading.
    '''
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def handle_trading_status(bot, message):
  wallets = main_api.get_wallets(message.chat.id)
  buy_wallet = wallets[result['wallet']]['id']
  if result['status'] == 1:
    result['status'] = 0
    bot.send_message(chat_id=message.chat.id,
                     text='Auto Swing Trading Stopped.')
    main_api.stop_auto_swing(message.chat.id)
  elif result['status']==0:
    result['status'] = 1
    bot.send_message(chat_id=message.chat.id,
                     text='Auto Swing Trading Started.')
    main_api.start_auto_swing(message.chat.id, result['buy_amount'], buy_wallet)
  keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
  bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def start_trading(bot, message):
  result['status'] = 1
  print(result['wallet'], result['buy_amount'], result['status'])