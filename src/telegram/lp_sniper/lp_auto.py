from telebot import types

from src.database import user as user_model
from src.engine import api as main_api
import threading
chain_buy_amounts = [0.1]
chain_gas_prices = [0.1, 0.2, 0.3]
chain_slippages = [50]
chain_counts = [100]
chain_limit_token_prices = [500, 1000, 2000]

chain_auto_sell_params = [{'amount': 100, 'price': 0}, {'amount': 50, 'price': 0}]
x_value_list = {'mode':0,'profit':0,"buy-amount": 0, 'slippage': 0, "stop-loss":0,
                "auto_amount":0, "auto_price":0,'max_mc':0, 'min_mc':0, 'token_count':0}

index_list = {'wallet': 100, 'buy_amount': 100, 'slippage': 100, 'profit':100, 'token_count':100}

result = {'wallet': 0, 'token': '', 'buy_amount': 0, 'slippage': 0,
          'stop-loss':0, 'max_mc':0, 'min_mc':0, 'profit':0, 'token_count':0, 'mode':0}

auto_sell_status = {'index':0}

global_text =  '''
*🎯 LP Sniper* >> Auto Mode

Introducing our LP Sniper function: a powerful tool designed
to automatically and accurately snipe liquidity pools,
providing you with the best entry points to maximize your
trading efficiency and returns.
    '''
def initialize_x_value():
    x_value_list['buy-amount'] = 0
    x_value_list['gas-amount'] = 0
    x_value_list['gas-price'] = 0
    x_value_list['limit-token-price'] = 0
    x_value_list['slippage'] = 0

def handle_start(bot, message):
   # user_model.create_user_by_telegram(message.chat.id)
    text = global_text
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def get_keyboard(update_data, chat_id, index_data):
    keyboard = types.InlineKeyboardMarkup()

    wallets = []

    chain_wallets = main_api.get_wallets(chat_id)
    wallet_count = len(chain_wallets)
    for index in range(wallet_count):
        caption = f'{"🟢" if index == index_data['wallet'] else ""} W{
            index + 1}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"lp auto select buy wallet {index}")
        wallets.append(button)
    more_wallet_btn = types.InlineKeyboardButton('🔽', callback_data='show more wallets')
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
            text=caption, callback_data=f"lp auto select buy amount {index}")
        buys.append(button)

    if update_data['buy-amount'] == 0:
        caption = "X SOL"
    else:
        caption = f"🟢 {update_data['buy-amount']} SOL"
    buy_x = types.InlineKeyboardButton(
        text=caption, callback_data='lp auto select buy amount x')

    slippage_title = types.InlineKeyboardButton(
        'Slippage:', callback_data='set title')
    slippages = []
    slip_page_count = len(chain_slippages)
    for index in range(slip_page_count):
        if index_data['slippage'] == 100:
            caption = f'Auto Slippage'
        else:
            caption = f'{"🟢" if index == index_data['slippage'] else ""} Auto Slippage'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"lp auto select slippage {index}")
        slippages.append(button)
    if update_data['slippage'] == 0:
        caption = "X% Slippage"
    else:
        caption = f"🟢 {update_data['slippage']}% Slippage"
    slippage_x = types.InlineKeyboardButton(
        text=caption, callback_data='lp auto select slippage x')

    
    max_mc_title = types.InlineKeyboardButton(text='Max MC:', callback_data='set title')
    min_mc_title = types.InlineKeyboardButton(text='Min MC:', callback_data='set title')
    if update_data['max_mc'] == 0:
        caption = "X"
    else:
        caption = f"{update_data['max_mc']}"
    max_mc_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper input market capital max_mc')
    if update_data['min_mc'] == 0:
        caption = "X"
    else:
        caption = f"{update_data['min_mc']}"
    min_mc_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper input market capital min_mc')
    
    token_count_title = types.InlineKeyboardButton(text='Token Count:', callback_data='set title')
    counts = []
    token_count = len(chain_counts)
    for index in range(token_count):
        if index_data['token_count'] == 100:
            caption = f'{chain_counts[index]}'
        else:
            caption = f'{"🟢" if index == index_data['token_count'] else ""} {
                chain_counts[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select token count {index}")
        counts.append(button)
    if update_data['token_count'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['token_count']}"
    token_count_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select token count x')
      
    create_order = types.InlineKeyboardButton(
        '✔️ Set Sniper', callback_data='make lp sniper order')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    if wallet_count <= 3:
      keyboard.row(*wallets[0:(wallet_count)])
    else:
      keyboard.row(*wallets[0:3], more_wallet_btn)

    keyboard.row(amount_title, *buys[0:buy_count], buy_x)
    keyboard.row(*slippages[0:(len(slippages))], slippage_x)
    keyboard.row(create_order)
    keyboard.row(back, close)

    return keyboard
  
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

def select_token_count(bot, message, index):
   # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    index_list['token_count'] = int(index)
    result['token_count'] = chain_counts[int(index)]
    x_value_list['token_count'] = 0

    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
    
def handle_select_auto_slippage(bot, message, index):
  text = '''
      *🎯 LP Sniper*
 Do you confirm 50% slippage as Auto Slippage?.
'''
  keyboard = types.InlineKeyboardMarkup()
  cancel = types.InlineKeyboardButton('Cancel', callback_data='lp auto select slippage x')
  confirm = types.InlineKeyboardButton('Confirm', callback_data=f'lp auto confirm select slippage {index}')
  keyboard.row(cancel, confirm)
  bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                    reply_markup=keyboard, disable_web_page_preview=True)
  bot.delete_message(chat_id=message.chat.id,
                       message_id=message.message_id)
  
def select_slip_page(bot, message, index):
   # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    index_list['slippage'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['slippage'] = chain_slippages[int(index)]
    x_value_list['slippage'] = 0

    text = global_text
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def handle_buy_amount_x(bot, message):
    text = '''
*LP Sniper > 💰 X*
Enter the amount to snipe:
'''
    item = "Buy Amount"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_slippage_x(bot, message):
    text = '''
*LP Sniper > 💧 X%*
Enter the slippage to set:
'''
    item = "Slippage"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_profit_x(bot, message):
    text = '''
*LP Sniper > X%*
Enter the amount of profit to set:
'''
    item = "Profit"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_token_count_x(bot, message):
    text = '''
*LP Sniper > X*
Enter the number of tokens to set:
'''
    item = "Token Count"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))
        
def handle_stop_loss_x(bot, message):
    text = '''
*LP Sniper > 💰 X*
Enter the Stop Loss Amount to set:
'''
    item = "Stop Loss"
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
    elif item == "Slippage":
        slippage_x = int(message.text)
        x_value_list['slippage'] = slippage_x
        result['slippage'] = slippage_x
        index_list['slippage'] = 100
    elif item == "Stop Loss":
        slippage_x = int(message.text)
        x_value_list['stop-loss'] = slippage_x
        result['stop-loss'] = slippage_x
    elif item == "Profit":
        slippage_x = float(message.text)
        x_value_list['profit'] = slippage_x
        result['profit'] = slippage_x
        index_list['profit'] = 100
    elif item == "Token Count":
        slippage_x = float(message.text)
        x_value_list['token_count'] = slippage_x
        result['token_count'] = slippage_x
        index_list['token_count'] = 100
        
    text = global_text
    
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def handle_set_sniper(bot, message):
  print(result['buy_amount'], result['slippage'])
  bot.send_message(chat_id=message.chat.id,
                     text='Successfully registered Sniper')
