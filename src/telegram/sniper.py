from telebot import types

from src.database import user as user_model
from src.engine import api as main_api
import threading
chain_buy_amounts = [0.1]
chain_gas_prices = [0.1, 0.2, 0.3]
chain_slippages = [50]
chain_profits = [5]
chain_counts = [100]
chain_limit_token_prices = [500, 1000, 2000]

chain_auto_sell_params = [{'amount': 100, 'price': 0}, {'amount': 50, 'price': 0}]
x_value_list = {'mode':0,'profit':0,"buy-amount": 0, 'slippage': 0, "stop-loss":0,
                "auto_amount":0, "auto_price":0,'max_mc':0, 'min_mc':0, 'token_count':0}

index_list = {'wallet': 100, 'buy_amount': 100, 'slippage': 100, 'profit':100, 'token_count':100}

result = {'wallet': 0, 'token': '', 'buy_amount': 0, 'slippage': 0,
          'stop-loss':0, 'max_mc':0, 'min_mc':0, 'profit':0, 'token_count':0, 'mode':0}

auto_sell_status = {'index':0}

def initialize_x_value():
    x_value_list['buy-amount'] = 0
    x_value_list['gas-amount'] = 0
    x_value_list['gas-price'] = 0
    x_value_list['limit-token-price'] = 0
    x_value_list['slippage'] = 0

def handle_sniper(bot, message):
   # user_model.create_user_by_telegram(message.chat.id)
    text = '''
*🎯 Token Sniper*

Select mode for token sniper here.
    '''

    keyboard = types.InlineKeyboardMarkup()
    
    auto_mode_btn = types.InlineKeyboardButton(
      text="🎮 Auto Mode", callback_data=f"sniper select auto mode")
    paste_mode_btn = types.InlineKeyboardButton(
      text="🤏 Manual Mode", callback_data=f"sniper select manual mode")
    
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    
    keyboard.row(auto_mode_btn, paste_mode_btn)
    keyboard.row(back, close)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def handle_manual_mode(bot, message):
   # user_model.create_user_by_telegram(message.chat.id)
    text = '''
🎯 * Token Sniper* >> Manual Mode

Enter a token symbol or address to snipe.
    '''
    x_value_list['mode'] = 1
    result['mode'] = 1
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_token(bot, next_message))
    bot.delete_message(chat_id=message.chat.id,
                       message_id=message.message_id)

def handle_auto_mode(bot, message):
   # user_model.create_user_by_telegram(message.chat.id)
    text = '''
🎯 * Token Sniper* >> Auto Mode

Set your parameters for auto token snipping.
    '''
    x_value_list['mode'] = 0
    result['mode'] = 0
    keyboard = get_keyboard(x_value_list,
                              message.chat.id, index_list)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def get_keyboard(update_data, chat_id, index_data):
   # wallet_count = 4
    # buy_count = 4
    # gas_amount_count = 3

    keyboard = types.InlineKeyboardMarkup()

    wallets = []

    chain_wallets = main_api.get_wallets(chat_id)
    wallet_count = len(chain_wallets)
    for index in range(wallet_count):
        caption = f'{"🟢" if index == index_data['wallet'] else ""} W{
            index + 1}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select buy wallet {index}")
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
            text=caption, callback_data=f"sniper select buy amount {index}")
        buys.append(button)

    if update_data['buy-amount'] == 0:
        caption = "X SOL"
    else:
        caption = f"🟢 {update_data['buy-amount']} SOL"
    buy_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select buy amount x')

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
            text=caption, callback_data=f"sniper select slippage {index}")
        slippages.append(button)
    if update_data['slippage'] == 0:
        caption = "X% Slippage"
    else:
        caption = f"🟢 {update_data['slippage']}% Slippage"
    slippage_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select slippage x')

    profit_title = types.InlineKeyboardButton(text='Profit:', callback_data='set title')
    profits = []
    profit_count = len(chain_profits)
    for index in range(profit_count):
        if index_data['profit'] == 100:
            caption = f'{chain_profits[index]}x'
        else:
            caption = f'{"🟢" if index == index_data['profit'] else ""} {
                chain_profits[index]}x'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"sniper select profit {index}")
        profits.append(button)
    if update_data['profit'] == 0:
        caption = "X"
    else:
        caption = f"🟢 {update_data['profit']}x"
    profit_x = types.InlineKeyboardButton(
        text=caption, callback_data='sniper select profit x')

    
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
    
    auto_sell = types.InlineKeyboardButton(
        '🔻 Auto Sell', callback_data='sniper set auto_sell')
    
    auto_amount_title = types.InlineKeyboardButton(
        'Amount:', callback_data='2')
    auto_price_title = types.InlineKeyboardButton(
        'Profit:', callback_data='2')
    auto_add_button = types.InlineKeyboardButton(
        'Add', callback_data='sniper add auto params')


    auto_amounts = []
    for index in range(len(chain_auto_sell_params)):
      auto_amount_x = types.InlineKeyboardButton(
          text=f'''{chain_auto_sell_params[index]['amount']}%''', callback_data=f'sniper select auto amount {index}')
      auto_amounts.append(auto_amount_x)
    
    auto_prices = []
    for index in range(len(chain_auto_sell_params)):
      auto_price_x = types.InlineKeyboardButton(
          text=f'''{chain_auto_sell_params[index]['price']}x''', callback_data=f'sniper select auto price {index}')
      auto_prices.append(auto_price_x)

    auto_removes = []
    for index in range(len(chain_auto_sell_params)):
      auto_remove_x = types.InlineKeyboardButton(
          text='remove', callback_data=f'sniper remove auto params {index}')
      auto_removes.append(auto_remove_x)
      
    create_order = types.InlineKeyboardButton(
        '✔️ Set Sniper', callback_data='make sniper order')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    if wallet_count <= 3:
      keyboard.row(*wallets[0:(wallet_count)])
    else:
      keyboard.row(*wallets[0:3], more_wallet_btn)

    keyboard.row(amount_title, *buys[0:buy_count], buy_x)
    keyboard.row(*slippages[0:(len(slippages))], slippage_x)
    keyboard.row(min_mc_title, min_mc_x, max_mc_title, max_mc_x)
    if update_data['mode'] == 0:
      keyboard.row(token_count_title, *counts[0:(len(counts))], token_count_x)
    keyboard.row(auto_sell)
    if auto_sell_status['index'] == 1:
      for index in range(len(chain_auto_sell_params)):
        keyboard.row(auto_amount_title, auto_amounts[index], auto_price_title, auto_prices[index], auto_removes[index])
      keyboard.row(auto_add_button)
    keyboard.row(create_order)
    keyboard.row(back, close)

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
      *🎯 Token Sniper*
❌ Not a token address.
'''
      keyboard = types.InlineKeyboardMarkup()
      retry = types.InlineKeyboardButton('Retry', callback_data='sniper select manual mode')
      back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
      keyboard.row(retry, back)
    else:
      #pool_data = main_api.check_liveness(message.chat.id, token)
      meta_data = main_api.get_token_metadata(message.chat.id, token)
      
      token_price = format_number(token_data['price'])
      token_liquidity = format_number(token_data['liquidity'])
      token_market_cap = format_number(token_data['market_cap'])
      text = f'''
      *🎯 Token Sniper*

Sell your tokens here.

*{meta_data['name']}  (🔗{current_chain})  *
{token}
      
*💲 Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
  '''
      keyboard = get_keyboard(x_value_list,
                              message.chat.id, index_list)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def handle_auto_sell(bot, message):
    if x_value_list['mode'] == 0:
      text = '''
🎯 * Token Sniper* >> Auto Mode

Set your parameters for auto token snipping.
    '''
    if x_value_list['mode'] == 1:
      chain_index = main_api.get_chain(message.chat.id)
      chains = main_api.get_chains()
      current_chain = chains[chain_index]
      token = result['token']
      token_data = main_api.get_token_market_data(message.chat.id, token)
      meta_data = main_api.get_token_metadata(message.chat.id, token)
      
      token_price = format_number(token_data['price'])
      token_liquidity = format_number(token_data['liquidity'])
      token_market_cap = format_number(token_data['market_cap'])
      text = f'''
      *🎯 Token Sniper*

  Sell your tokens here.

  *{meta_data['name']}  (🔗{current_chain})  *
  {token}
      
  💲 *Price:* {token_price}$
  💧 *Liquidity:* {token_liquidity}$
  📊 *Market Cap:* {token_market_cap}$

  [Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
  '''
    if auto_sell_status['index'] == 0:
      auto_sell_status['index'] = 1
    elif auto_sell_status['index'] == 1:
      auto_sell_status['index'] = 0

    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    bot.delete_message(chat_id=message.chat.id,
                       message_id=message.message_id)
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

def select_profit(bot, message, index):
   # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]
    index_list['profit'] = int(index)
    result['profit'] = chain_profits[int(index)]
    x_value_list['profit'] = 0

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
      *🎯 Token Sniper*
 Do you confirm 50% slippage as Auto Slippage?.
'''
  keyboard = types.InlineKeyboardMarkup()
  cancel = types.InlineKeyboardButton('Cancel', callback_data='sniper select slippage x')
  confirm = types.InlineKeyboardButton('Confirm', callback_data=f'sniper confirm select slippage {index}')
  keyboard.row(cancel, confirm)
  bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                    reply_markup=keyboard, disable_web_page_preview=True)
  
def select_slip_page(bot, message, index):
   # user = user_model.get_user_by_telegram(message.chat.id)
   # chain = user.chain
    #  wallets = user.wallets[chain]

    index_list['slippage'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['slippage'] = chain_slippages[int(index)]
    x_value_list['slippage'] = 0
    
    if x_value_list['mode'] == 0:
      text = '''
🎯 * Token Sniper* >> Auto Mode

Set your parameters for auto token snipping.
    '''
    if x_value_list['mode'] == 1:
      chain_index = main_api.get_chain(message.chat.id)
      chains = main_api.get_chains()
      current_chain = chains[chain_index]
      token = result['token']
      token_data = main_api.get_token_market_data(message.chat.id, token)
      meta_data = main_api.get_token_metadata(message.chat.id, token)
      
      token_price = format_number(token_data['price'])
      token_liquidity = format_number(token_data['liquidity'])
      token_market_cap = format_number(token_data['market_cap'])
      text = f'''
      *🎯 Token Sniper*

  Sell your tokens here.

  *{meta_data['name']}  (🔗{current_chain})  *
  {token}
      
  💲 *Price:* {token_price}$
  💧 *Liquidity:* {token_liquidity}$
  📊 *Market Cap:* {token_market_cap}$

  [Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
  '''
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def handle_buy_amount_x(bot, message):
    text = '''
*Token Sniper > 💰 X*
Enter the amount to snipe:
'''
    item = "Buy Amount"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))


def handle_slippage_x(bot, message):
    text = '''
*Token Sniper > 💧 X%*
Enter the slippage to set:
'''
    item = "Slippage"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_profit_x(bot, message):
    text = '''
*Token Sniper > X%*
Enter the amount of profit to set:
'''
    item = "Profit"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_token_count_x(bot, message):
    text = '''
*Token Sniper > X*
Enter the number of tokens to set:
'''
    item = "Token Count"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))
        
def handle_stop_loss_x(bot, message):
    text = '''
*Token Sniper > 💰 X*
Enter the Stop Loss Amount to set:
'''
    item = "Stop Loss"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_auto_amount_value(bot, message,index):
    text = '''
*Token Sniper > 💰 X*
Enter the Amount to set:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_auto_amount_input_value(bot, next_message, index))

def handle_auto_price_value(bot, message,index):
    text = '''
*Token Sniper > 💰 X*
Enter the Price to set:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_auto_price_input_value(bot, next_message, index))


def handle_auto_amount_input_value(bot, message, index):
    item = int(index)
    chain_auto_sell_params[item]['amount'] = message.text
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    token = 0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7

    chain = 'ethereum'

    name = "elo"
    text = f'''
            *Token Sniper*

    Sell your tokens here.

     *{name}  (🔗{chain})*
      {token}
      ❌ Snipe not set

      [Scan](https://etherscan.io/address/{token}) | [Dexscreener](https://dexscreener.com/ethereum/{token}) | [DexTools](https://www.dextools.io/app/en/ether/pair-explorer/{token}) | [Defined](https://www.defined.fi/eth/{token})
          '''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def handle_auto_price_input_value(bot, message, index):
    item = int(index)
    chain_auto_sell_params[item]['price'] = message.text
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    chain_index = main_api.get_chain(message.chat.id)
    chains = main_api.get_chains()
    current_chain = chains[chain_index]
    token = result['token']
    token_data = main_api.get_token_market_data(message.chat.id, token)
    meta_data = main_api.get_token_metadata(message.chat.id, token)
    
    token_price = format_number(token_data['price'])
    token_liquidity = format_number(token_data['liquidity'])
    token_market_cap = format_number(token_data['market_cap'])
    text = f'''
    *🎯 Token Sniper*

Sell your tokens here.

*{meta_data['name']}  (🔗{current_chain})  *
{token}
    
💲 *Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def handle_input_value(bot, message, item):
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
        
    if x_value_list['mode'] == 0:
      text = '''
🎯 * Token Sniper* >> Auto Mode

Set your parameters for auto token snipping.
    '''
    if x_value_list['mode'] == 1:
      chain_index = main_api.get_chain(message.chat.id)
      chains = main_api.get_chains()
      current_chain = chains[chain_index]
      token = result['token']
      token_data = main_api.get_token_market_data(message.chat.id, token)
      meta_data = main_api.get_token_metadata(message.chat.id, token)
      
      token_price = format_number(token_data['price'])
      token_liquidity = format_number(token_data['liquidity'])
      token_market_cap = format_number(token_data['market_cap'])
      text = f'''
      *🎯 Token Sniper*

  Sell your tokens here.

  *{meta_data['name']}  (🔗{current_chain})  *
  {token}
      
  💲 *Price:* {token_price}$
  💧 *Liquidity:* {token_liquidity}$
  📊 *Market Cap:* {token_market_cap}$

  [Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
  '''
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def input_market_cap(bot, message, item):
    text = '''
*Token Sniper > X*
Enter the market cap to set:
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_market_cap(bot, next_message, item))

def handle_input_market_cap(bot, message, item):
    result[item] = int(message.text)
    x_value_list[item] = int(message.text)

    if x_value_list['mode'] == 0:
      text = '''
🎯 * Token Sniper* >> Auto Mode

Set your parameters for auto token snipping.
    '''
    if x_value_list['mode'] == 1:
      chain_index = main_api.get_chain(message.chat.id)
      chains = main_api.get_chains()
      current_chain = chains[chain_index]
      token = result['token']
      token_data = main_api.get_token_market_data(message.chat.id, token)
      meta_data = main_api.get_token_metadata(message.chat.id, token)
      
      token_price = format_number(token_data['price'])
      token_liquidity = format_number(token_data['liquidity'])
      token_market_cap = format_number(token_data['market_cap'])
      text = f'''
      *🎯 Token Sniper*

  Sell your tokens here.

  *{meta_data['name']}  (🔗{current_chain})  *
  {token}
      
  💲 *Price:* {token_price}$
  💧 *Liquidity:* {token_liquidity}$
  📊 *Market Cap:* {token_market_cap}$

  [Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
  '''
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
     

def handle_remove_auto_params(bot, message, index):
    item = int(index)
    chain_auto_sell_params.pop(item)
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    chain_index = main_api.get_chain(message.chat.id)
    chains = main_api.get_chains()
    current_chain = chains[chain_index]
    token = result['token']
    token_data = main_api.get_token_market_data(message.chat.id, token)
    meta_data = main_api.get_token_metadata(message.chat.id, token)
    
    token_price = format_number(token_data['price'])
    token_liquidity = format_number(token_data['liquidity'])
    token_market_cap = format_number(token_data['market_cap'])
    text = f'''
    *🎯 Token Sniper*

Sell your tokens here.

*{meta_data['name']}  (🔗{current_chain})  *
{token}
    
💲 *Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)

def add_auto_param(bot, message):
    new_param = {'amount':0, 'price':0}
    chain_auto_sell_params.append(new_param)
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    chain_index = main_api.get_chain(message.chat.id)
    chains = main_api.get_chains()
    current_chain = chains[chain_index]
    token = result['token']
    token_data = main_api.get_token_market_data(message.chat.id, token)
    meta_data = main_api.get_token_metadata(message.chat.id, token)
    
    token_price = format_number(token_data['price'])
    token_liquidity = format_number(token_data['liquidity'])
    token_market_cap = format_number(token_data['market_cap'])
    text = f'''
    *🎯 Token Sniper*

Sell your tokens here.

*{meta_data['name']}  (🔗{current_chain})  *
{token}
    
💲 *Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
'''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    
def handle_set_sniper(bot, message):
  print(result['buy_amount'], result['slippage'], result['min_mc'], result['max_mc'], result['profit'])
  bot.send_message(chat_id=message.chat.id,
                     text='Successfully registered Sniper')

