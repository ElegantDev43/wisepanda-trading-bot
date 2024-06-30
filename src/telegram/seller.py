from telebot import types

from src.engine import api as main_api
from src.telegram import user_manage as feature_api


current_keyboard = {}
order_captions = ['Market', 'Limit', 'DCA']
def format_number(num):
    if num >= 1_000_000_000:
        formatted_num = f"{num / 1_000_000_000:.3f}B"
    elif num >= 1_000_000:
        formatted_num = f"{num / 1_000_000:.3f}M"
    elif num >= 1_000:
        formatted_num = f"{num / 1_000:.3f}K"
    else:
        formatted_num = f"{num:.18f}"
    return formatted_num


def handle_start(bot, message):
  
    chain_positions = main_api.get_positions(message.chat.id)
    text = f'''
            *🛒 Token Sell*
            
You currently have {len(chain_positions)} positions.

Select position to sell tokens.
'''
    feature_api.initialize_values(message.chat.id, 'seller')
    keyboard_data = feature_api.get_user_feature_values(message.chat.id, 'seller')
    current_keyboard.update(keyboard_data)
    keyboard = types.InlineKeyboardMarkup()
    positions = []
    chain_positions = main_api.get_positions(message.chat.id)
    position_count = len(chain_positions)
    wallets = main_api.get_wallets(message.chat.id)
    for index in range(position_count):
      for item in range(len(wallets)):
        if wallets[item]['id'] == chain_positions[index]['wallet_id']:
          meta = main_api.get_token_metadata(message.chat.id, chain_positions[index]['token'])
          caption = f'Token: {meta['symbol']}, Amount:{chain_positions[index]['amount']}, W{item + 1}'
      button = types.InlineKeyboardButton(
            text=caption, callback_data=f"seller select position {index}")
      positions.append(button)
    for item in positions:
      keyboard.row(item)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def get_keyboard(chat_id, keyboard_data):
    keyboard = types.InlineKeyboardMarkup()

    if keyboard_data['order_name'] == 0:
      market_caption = '✅ Market'
      limit_caption = 'Limit'
      dca_caption = 'DCA'
    elif keyboard_data['order_name'] == 1:
      market_caption = 'Market'
      limit_caption = '✅ Limit'
      dca_caption = 'DCA'
    elif keyboard_data['order_name'] == 2:
      market_caption = 'Market'
      limit_caption = 'Limit'
      dca_caption = '✅ DCA'

    market_order = types.InlineKeyboardButton(text= market_caption, callback_data='seller market_order')
    limit_order = types.InlineKeyboardButton(text= limit_caption, callback_data='seller limit_order')
    dca_order = types.InlineKeyboardButton(text= dca_caption, callback_data='seller dca_order')
    
    buy_amount = types.InlineKeyboardButton(
        text="🟢 100%" if keyboard_data['amount'] == 100 else "100%", callback_data='seller amount default')
    if keyboard_data['amount'] == -999:
      caption = 'X% ✏️'
    elif keyboard_data['amount'] == 100:
      caption = 'X% ✏️'
    else:
      caption = f'''🟢 {keyboard_data['amount']}%'''
    buy_amount_x = types.InlineKeyboardButton(
        text=caption, callback_data='seller amount x')

    slippage = types.InlineKeyboardButton(
        text="🟢 Auto Slippage" if keyboard_data['slippage'] == 50 else "Auto Slippage", callback_data='seller slippage default')
    if keyboard_data['slippage'] == -999:
      caption = 'X Slippage ✏️'
    elif keyboard_data['slippage'] == 50:
      caption = 'X Slippage ✏️'
    else:
      caption = f'''🟢 {keyboard_data['slippage']}% Slippage'''
    slippage_x = types.InlineKeyboardButton(
        text=caption, callback_data='seller slippage x')

    if keyboard_data['profit'] == 0:
      caption = "✏️ Profit: _"
    else:
      caption = f"✏️ Profit: {keyboard_data['profit']}"
    profit = types.InlineKeyboardButton(
          text=caption, callback_data='seller profit')

    if keyboard_data['interval'] == 0:
      caption = "✏️ Interval: _"
    else:
      caption = f"✏️ Interval: {keyboard_data['interval']}"
    interval = types.InlineKeyboardButton(
          text=caption, callback_data='seller interval')
    
    if keyboard_data['count'] == 0:
      caption = "✏️ Count: _"
    else:
      caption = f"✏️ Count: {keyboard_data['count']}"
    count = types.InlineKeyboardButton(
          text=caption, callback_data='seller count')

    create_order = types.InlineKeyboardButton(
        '✔️ Buy', callback_data='seller make order')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')


    keyboard.row(market_order, limit_order, dca_order)
    
    keyboard.row(buy_amount, buy_amount_x)
    keyboard.row(slippage, slippage_x)
    if keyboard_data['order_name'] == 1:
      keyboard.row(profit)
    elif keyboard_data['order_name'] == 2:
      keyboard.row(interval, count)
    keyboard.row(create_order)
    keyboard.row(back, close)

    return keyboard


def handle_select_position(bot, message, index):
    chain_positions = main_api.get_positions(message.chat.id)
    current_keyboard['wallet'] = chain_positions[int(index)]['id']
    current_keyboard['token'] = chain_positions[int(index)]['token']
    feature_api.update_user_feature_values(message.chat.id, 'seller', current_keyboard)
    chain_index = main_api.get_chain(message.chat.id)
    chains = main_api.get_chains()
    current_chain = chains[chain_index]
    token = current_keyboard['token']
    token_data = main_api.get_token_market_data(message.chat.id, token)
    meta_data = main_api.get_token_metadata(message.chat.id, token)
    token_price = format_number(token_data['price'])
    token_liquidity = format_number(token_data['liquidity'])
    token_market_cap = format_number(token_data['market_capital'])
    text = f'''
    *🛒 Token Sell*

Sell your tokens here.

*{meta_data['name']}  (🔗{current_chain})  *
{token}

💲 *Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
'''

    keyboard = get_keyboard(message.chat.id, current_keyboard)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def handle_default_values(bot, message, item):
    current_keyboard[item] = 100
    #print(current_keyboard)
    feature_api.update_user_feature_values(message.chat.id, 'seller', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_x_values(bot, message, item):
    text = f'''
*🛒 Token Sell*
Enter the {item} to set:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_input_value(bot, message, item):
    if item == 'amount':
      current_keyboard[item] = int(message.text)
    elif item == 'slippage':
      current_keyboard[item] = int(message.text)
    elif item == 'stop-loss':
      current_keyboard[item] = int(message.text)
    #print(current_keyboard)
    else:
      current_keyboard[item] = int(message.text)

    feature_api.update_user_feature_values(message.chat.id, 'seller', current_keyboard)
    chain_index = main_api.get_chain(message.chat.id)
    chains = main_api.get_chains()
    current_chain = chains[chain_index]
    token = current_keyboard['token']
    token_data = main_api.get_token_market_data(message.chat.id, token)
    meta_data = main_api.get_token_metadata(message.chat.id, token)
    token_price = format_number(token_data['price'])
    token_liquidity = format_number(token_data['liquidity'])
    token_market_cap = format_number(token_data['market_capital'])
    text = f'''
    *🛒 Token Sell*

Sell your tokens here.

*{meta_data['name']}  (🔗{current_chain})  *
{token}

💲 *Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
'''

    keyboard = get_keyboard(message.chat.id, current_keyboard)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def handle_confirm_auto_slippage(bot, message):
  text = '''
      *🛒 Token Sell*
 Do you confirm maximum of 50% slippage as Auto Slippage?.
'''
  keyboard = types.InlineKeyboardMarkup()
  cancel = types.InlineKeyboardButton('Cancel', callback_data='seller slippage x')
  confirm = types.InlineKeyboardButton('Confirm', callback_data=f'seller slippage confirm')
  keyboard.row(cancel, confirm)
  bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                    reply_markup=keyboard, disable_web_page_preview=True)

def handle_default_slippage(bot, message):
    current_keyboard['slippage'] = 50

    chain_index = main_api.get_chain(message.chat.id)
    chains = main_api.get_chains()
    current_chain = chains[chain_index]
    token = current_keyboard['token']
    token_data = main_api.get_token_market_data(message.chat.id, token)
    meta_data = main_api.get_token_metadata(message.chat.id, token)
    token_price = format_number(token_data['price'])
    token_liquidity = format_number(token_data['liquidity'])
    token_market_cap = format_number(token_data['market_capital'])
    text = f'''
    *🛒 Token Sell*

Sell your tokens here.

*{meta_data['name']}  (🔗{current_chain})  *
{token}

💲 *Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
'''

    keyboard = get_keyboard(message.chat.id, current_keyboard)
    feature_api.update_user_feature_values(message.chat.id, 'seller', current_keyboard)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def select_wallet(bot, message, index):
    current_keyboard['wallet'] = int(index)
    feature_api.update_user_feature_values(message.chat.id, 'seller', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_show_more_wallets(bot, message):
    current_keyboard['wallet_row'] += 1
    feature_api.update_user_feature_values(message.chat.id, 'seller', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_market_order(bot, message):
    current_keyboard['order_name'] = 0
    feature_api.update_user_feature_values(message.chat.id, 'seller', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_limit_order(bot, message):
    current_keyboard['order_name'] = 1
    feature_api.update_user_feature_values(message.chat.id, 'seller', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_dca_order(bot, message):
    current_keyboard['order_name'] = 2
    feature_api.update_user_feature_values(message.chat.id, 'seller', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
    
def handle_make_order(bot, message):
  
    wallets = main_api.get_wallets(message.chat.id)
    buy_amount = int(current_keyboard['amount'])
    if current_keyboard['order_name'] == 0:
        tx_id, amount = main_api.market_sell(message.chat.id, current_keyboard['wallet'], buy_amount, current_keyboard['slippage'])
        result_text = f'''Successfully confirmed Buy Transaction.
Transaction ID: {tx_id}
View on SolScan: (https://solscan.io/tx/{tx_id})'''
        bot.send_message(chat_id=message.chat.id,
                     text=result_text)
    elif current_keyboard['order_name'] == 1:
        main_api.add_limit_sell(message.chat.id, current_keyboard['wallet'], buy_amount, current_keyboard['slippage'],current_keyboard['profit'])
        bot.send_message(chat_id=message.chat.id,
                     text='Successfully registered Order.')
    elif current_keyboard['order_name'] == 2:
        main_api.add_dca_sell(message.chat.id, current_keyboard['wallet'], buy_amount, current_keyboard['slippage'],  current_keyboard['interval'], current_keyboard['count'])
        bot.send_message(chat_id=message.chat.id,
                     text='Successfully registered Order.')