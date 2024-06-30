from telebot import types

from src.engine import api as main_api
from src.telegram import user_manage as feature_api


current_keyboard = {}
auto_sell_status = {'status':0}

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
   # user_model.create_user_by_telegram(message.chat.id)
    text = '''
  *🎯 Token Sniper* >> Manual Mode

Enter a token address to buy.
    '''
    feature_api.initialize_values(message.chat.id, 'token_sniper_manual')
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    keyboard_data = feature_api.get_user_feature_values(message.chat.id, 'token_sniper_manual')
    current_keyboard.update(keyboard_data)
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_token(bot, next_message))

def get_keyboard(chat_id, keyboard_data):
    keyboard = types.InlineKeyboardMarkup()
    wallets = []
    chain_wallets = main_api.get_wallets(chat_id)
    wallet_count = len(chain_wallets)
    for index in range(wallet_count):
        caption = f'{"🟢" if index == keyboard_data['wallet'] else ""} W{
            index + 1}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"token_sniper_manual select buy wallet {index}")
        wallets.append(button)
    more_wallet_btn = types.InlineKeyboardButton('🔽', callback_data='token_sniper_manual show more wallets')

    buy_amount = types.InlineKeyboardButton(
        text="🟢 1 SOL" if keyboard_data['amount'] == 10**9 else "1 SOL", callback_data='token_sniper_manual amount default')
    if keyboard_data['amount'] == -999:
      caption = 'X SOL ✏️'
    elif keyboard_data['amount'] == 10**9:
      caption = 'X SOL ✏️'
    else:
      caption = f'''🟢 {float(keyboard_data['amount'] / (10 ** 9))} SOL'''
    buy_amount_x = types.InlineKeyboardButton(
        text=caption, callback_data='token_sniper_manual amount x')

    slippage = types.InlineKeyboardButton(
        text="🟢 Auto Slippage" if keyboard_data['slippage'] == 50 else "Auto Slippage", callback_data='token_sniper_manual slippage default')
    if keyboard_data['slippage'] == -999:
      caption = 'X Slippage ✏️'
    elif keyboard_data['slippage'] == 50:
      caption = 'X Slippage ✏️'
    else:
      caption = f'''🟢 {keyboard_data['slippage']}% Slippage'''
    slippage_x = types.InlineKeyboardButton(
        text=caption, callback_data='token_sniper_manual slippage x')
    
    if keyboard_data['stop-loss'] == 0:
      caption = "✏️ Stop Loss: _"
    else:
      caption = f"✏️ Stop Loss: {keyboard_data['stop-loss']}%"
    stop_loss_x = types.InlineKeyboardButton(
          text=caption, callback_data='token_sniper_manual stop-loss')

    auto_sell = types.InlineKeyboardButton(
        '🔻 Set Auto Sell', callback_data='token_sniper_manual set auto_sell')

    auto_add_button = types.InlineKeyboardButton(
        'Add Sell Stage', callback_data='token_sniper_manual add auto params')
    auto_remove_button = types.InlineKeyboardButton(
        'Remove Sell Stage', callback_data='token_sniper_manual remove auto params')
    
    create_order = types.InlineKeyboardButton(
        '✔️ Set Sniper', callback_data='token_sniper_manual make order')
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
    keyboard.row(stop_loss_x)
    keyboard.row(auto_sell)
    if auto_sell_status['status'] == 1:
      keyboard.row(auto_add_button, auto_remove_button)
      for index in range(len(keyboard_data['chain_auto_sell_params'])):
        auto_amount = types.InlineKeyboardButton(
          f'✏️ Sell Amount(%): {keyboard_data['chain_auto_sell_params'][index]['amount']}%' if keyboard_data['chain_auto_sell_params'][index]['amount'] != 0 else '✏️ Sell Amount(%): _', callback_data=f'token_sniper_manual auto_sell {index}')
        auto_profit = types.InlineKeyboardButton(
          f'✏️ Sell Profit: {keyboard_data['chain_auto_sell_params'][index]['profit']}x' if keyboard_data['chain_auto_sell_params'][index]['profit'] != 0 else '✏️ Sell Profit: _', callback_data=f'token_sniper_manual auto_profit {index}')
        keyboard.row(auto_amount, auto_profit)
    keyboard.row(create_order)
    keyboard.row(back, close)

    return keyboard


def handle_input_token(bot, message):
    current_keyboard['token'] = message.text

    chain_index = main_api.get_chain(message.chat.id)
    chains = main_api.get_chains()
    current_chain = chains[chain_index]
    token = current_keyboard['token']
    if main_api.is_valid_token(message.chat.id, token) == False:
      text = '''
      *🎯 Token Sniper* >> Manual Mode
❌ Not a token address.
'''
      keyboard = types.InlineKeyboardMarkup()
      retry = types.InlineKeyboardButton('Retry', callback_data='token_sniper_manual')
      back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
      keyboard.row(retry, back)
      bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    else:
        #if main_api.check_token_liveness(message.chat.id, token):
          token_data = main_api.get_token_market_data(message.chat.id, token)
          meta_data = main_api.get_token_metadata(message.chat.id, token)
          token_price = format_number(token_data['price'])
          token_liquidity = format_number(token_data['liquidity'])
          token_market_cap = format_number(token_data['market_capital'])
          text = f'''
              *🎯 Token Sniper* >> Manual Mode

Buy your tokens here.

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
    current_keyboard[item] = 10**9
    #print(current_keyboard)
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_manual', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_x_values(bot, message, item):
    text = f'''
*🎯 Token Sniper* >> Manual Mode
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

    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_manual', current_keyboard)
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
    *🎯 Token Sniper* >> Manual Mode

Buy your tokens here.

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
      *🎯 Token Sniper* >> Manual Mode
 Do you confirm maximum of 50% slippage as Auto Slippage?.
'''
  keyboard = types.InlineKeyboardMarkup()
  cancel = types.InlineKeyboardButton('Cancel', callback_data='token_sniper_manual slippage x')
  confirm = types.InlineKeyboardButton('Confirm', callback_data=f'token_sniper_manual slippage confirm')
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
    *🎯 Token Sniper* >> Manual Mode

Buy your tokens here.

*{meta_data['name']}  (🔗{current_chain})  *
{token}

💲 *Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
'''

    keyboard = get_keyboard(message.chat.id, current_keyboard)
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_manual', current_keyboard)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def select_wallet(bot, message, index):
    current_keyboard['wallet'] = int(index)
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_manual', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_show_more_wallets(bot, message):
    current_keyboard['wallet_row'] += 1
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_manual', current_keyboard)
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
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_manual', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_remove_auto_sell_param(bot, message):
    length = len(current_keyboard['chain_auto_sell_params'])
    current_keyboard['chain_auto_sell_params'].pop(length-1)
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_manual', current_keyboard)
    keyboard = get_keyboard(message.chat.id, current_keyboard)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
    
def handle_auto_sell_input_values(bot, message, index):
    text = f'''
*🎯 Token Sniper* >> Manual Mode
Enter the amount to sell:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_auto_sell_inputs(bot, next_message, int(index)))
    
def handle_auto_sell_inputs(bot, message, index):
    current_keyboard['chain_auto_sell_params'][index]['amount'] = int(message.text)
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
    *🎯 Token Sniper* >> Manual Mode

Buy your tokens here.

*{meta_data['name']}  (🔗{current_chain})  *
{token}

💲 *Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
'''

    keyboard = get_keyboard(message.chat.id, current_keyboard)
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_manual', current_keyboard)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def handle_auto_profit_input_values(bot, message, index):
    text = f'''
*🎯 Token Sniper* >> Manual Mode
Enter the profit to get in sell:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_auto_profit_inputs(bot, next_message, int(index)))
    
def handle_auto_profit_inputs(bot, message, index):
    current_keyboard['chain_auto_sell_params'][index]['profit'] = int(message.text)
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
    *🎯 Token Sniper* >> Manual Mode

Buy your tokens here.

*{meta_data['name']}  (🔗{current_chain})  *
{token}

💲 *Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
'''

    keyboard = get_keyboard(message.chat.id, current_keyboard)
    feature_api.update_user_feature_values(message.chat.id, 'token_sniper_manual', current_keyboard)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def handle_make_order(bot, message):
  wallets = main_api.get_wallets(message.chat.id)
  buy_wallet = wallets[current_keyboard['wallet']]['id']
  main_api.add_token_sniper(message.chat.id, current_keyboard['token'], current_keyboard['amount'],current_keyboard['slippage'], buy_wallet, current_keyboard['chain_auto_sell_params'], current_keyboard['stop-loss'])
  bot.send_message(text = "successfully registered sniper")