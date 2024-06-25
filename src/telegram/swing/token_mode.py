from telebot import types
from src.engine import api as main_api

chain_buy_amounts = [100]

from src.database.swing import Htokens as HTokens_model


x_value_list = {"buy-amount": 0}

index_list = {'wallet': 100, 'buy_amount': 100}

result = {'wallet': 0, 'buy_amount': 0, 'status':0}

def handle_start(bot, message):
   # user_model.create_user_by_telegram(message.chat.id)
    text = '''
 *🪁 Swing Trading* >> Select Token Mode

Enter a token symbol or address to snipe.
    '''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_token(bot, next_message))
    bot.delete_message(chat_id=message.chat.id,
                       message_id=message.message_id)
    
def get_keyboard(update_data, chat_id, index_data):

    keyboard = types.InlineKeyboardMarkup()

    wallets = []

    chain_wallets = main_api.get_wallets(chat_id)
    wallet_count = len(chain_wallets)
    for index in range(wallet_count):
        caption = f'{"🟢" if index == index_data['wallet'] else ""} W{
            index + 1}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"token_mode swing select buy wallet {index}")
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
            text=caption, callback_data=f"token_mode swing select buy amount {index}")
        buys.append(button)

    start_btn = types.InlineKeyboardButton('Start', callback_data='start swing token_mode')
    stop_btn = types.InlineKeyboardButton('Stop', callback_data='stop swing auto mode')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='swing')
    if update_data['buy-amount'] == 0:
        caption = "X SOL"
    else:
        caption = f"🟢 {update_data['buy-amount']} SOL"
    buy_x = types.InlineKeyboardButton(
        text=caption, callback_data='token_mode swing select buy amount x')
    
    if wallet_count <= 3:
      keyboard.row(*wallets[0:(wallet_count)])
    else:
      keyboard.row(*wallets[0:3], more_wallet_btn)
    keyboard.row(amount_title, *buys[0:buy_count], buy_x)
    keyboard.row(start_btn, stop_btn)
    keyboard.row(back)
    return keyboard

def format_number(num):
    if num >= 1_000_000_000:
        formatted_num = f"{num / 1_000_000_000:.3f}B"
    elif num >= 1_000_000:
        formatted_num = f"{num / 1_000_000:.3f}M"
    elif num >= 1_000:
        formatted_num = f"{num / 1_000:.3f}K"
    else:
        formatted_num = f"{num:.3f}"
    return formatted_num
  
def handle_input_token(bot, message):
   # user = user_model.get_user_by_telegram(message.chat.id)

    result['token']=message.text
    
    chain_index = main_api.get_chain(message.chat.id)
    chains = main_api.get_chains()
    current_chain = chains[chain_index]
    token = result['token']
    token_data = main_api.get_token_market_data(message.chat.id, token)
    if token_data == 999:
      text = '''
      *🪁 Swing Trading* >> Select Token Mode
❌ Not a token address.
'''
      keyboard = types.InlineKeyboardMarkup()
      retry = types.InlineKeyboardButton('Retry', callback_data='swing mode select_token')
      back = types.InlineKeyboardButton('🔙 Back', callback_data='swing')
      keyboard.row(retry, back)
    else:
      #pool_data = main_api.check_liveness(message.chat.id, token)
      meta_data = main_api.get_token_metadata(message.chat.id, token)
      
      token_price = format_number(token_data['price'])
      token_liquidity = format_number(token_data['liquidity'])
      token_market_cap = format_number(token_data['market_capital'])
      text = f'''
      *🪁 Swing Trading* >> Select Token Mode

*{meta_data['name']}  (🔗{current_chain})  *
{token}
      
*💲 Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

'''
      keyboard = get_keyboard(x_value_list,
                              message.chat.id, index_list)
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
*Swing Trading(Select Token Mode) > 💰 X*
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
        
    chain_index = main_api.get_chain(message.chat.id)
    chains = main_api.get_chains()
    current_chain = chains[chain_index]
    token = result['token']
    token_data = main_api.get_token_market_data(message.chat.id, token)
    meta_data = main_api.get_token_metadata(message.chat.id, token)
    
    token_price = format_number(token_data['price'])
    token_liquidity = format_number(token_data['liquidity'])
    token_market_cap = format_number(token_data['market_capital'])
    text = f'''
      *🪁 Swing Trading* >> Select Token Mode

*{meta_data['name']}  (🔗{current_chain})  *
{token}
      
*💲 Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

'''
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
    
def start_trading(bot, message):
  result['status'] = 1
  print(result['wallet'], result['buy_amount'], result['status'])