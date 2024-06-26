from telebot import types

from src.database import user as user_model
from src.engine import api as main_api
import threading

chain_buy_amounts = [10]
chain_slippages = [50]

x_value_list = {"buy-amount": 0, "slippage": 0, 'more_btn_index':1}

index_list = {'wallet': 100, 'buy_amount': 100, 'slippage': 100}

result = {'wallet': 0, 'buy_amount': 0, 'slippage': 0, 'token':''}


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


def initialize_x_value():
    x_value_list['buy-amount'] = 0
    x_value_list['gas-amount'] = 0
    x_value_list['gas-price'] = 0
    x_value_list['limit-token-price'] = 0
    x_value_list['slippage'] = 0
    x_value_list['market-capital'] = 0
    x_value_list['liquidity'] = 0
    x_value_list['limit-tax'] = 0


def handle_start(bot, message):
   # user_model.create_user_by_telegram(message.chat.id)
    text = '''
    *🪁 Swing Trading* >> Manual Mode

Enter a token symbol or address to buy.
    '''
    x_value_list['more_btn_index'] = 1
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_token(bot, next_message))


def get_keyboard(update_data, chat_id, index_data):
   # wallet_count = 4
    # buy_count = 4
    # gas_amount_count = 3

    keyboard = types.InlineKeyboardMarkup()

    wallets = []
    more_wallet_btn = types.InlineKeyboardButton('🔽', callback_data='swing manual show more wallets')
    chain_wallets = main_api.get_wallets(chat_id)
    wallet_count = len(chain_wallets)
    for index in range(wallet_count):
        caption = f'{"🟢" if index == index_data['wallet'] else ""} W{
            index + 1}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f"manual swing select buy wallet {index}")
        wallets.append(button)
    wallet_all = types.InlineKeyboardButton(
        'All', callback_data=f'select buy wallet all')

    anti_mev = types.InlineKeyboardButton(
        '🔴 Anti-Mev', callback_data=f'anti mev')
    anti_rug = types.InlineKeyboardButton(
        '🔴 Anti-Rug', callback_data=f'anti Rug')

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
            text=caption, callback_data=f"manual swing select buy amount {index}")
        buys.append(button)

    if update_data['buy-amount'] == 0:
        caption = "X SOL"
    else:
        caption = f"🟢 {update_data['buy-amount']} SOL"
    buy_x = types.InlineKeyboardButton(
        text=caption, callback_data='manual swing select buy amount x')

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
            text=caption, callback_data=f"manual swing select slippage {index}")
        slippages.append(button)
    if update_data['slippage'] == 0:
        caption = "X% Slippage"
    else:
        caption = f"🟢 {update_data['slippage']}% Slippage"
    slippage_x = types.InlineKeyboardButton(
        text=caption, callback_data='manual swing select slippage x')

    create_order = types.InlineKeyboardButton(
        '✔️ Buy', callback_data='manual swing make buy order')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    
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

    current_chain_index = main_api.get_chain(chat_id)
    chains = main_api.get_chains()
    current_chain = chains[current_chain_index]
    keyboard.row(slippage_title, *
                     slippages[0:(len(slippages))], slippage_x)
    keyboard.row(create_order)
    keyboard.row(back, close)

    return keyboard

def handle_input_token(bot, message):
    result['token'] = message.text
    
    image_url = main_api.get_price_chart(result['token'])

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
    *🪁 Swing Trading* >> Manual Mode

*{meta_data['name']}  (🔗{current_chain})  *
{token}
    
💲 *Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
'''
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    with open(image_url, 'rb') as image:
        bot.send_photo(chat_id=message.chat.id, photo = image, caption=text, parse_mode='Markdown', reply_markup=keyboard)

def select_buy_wallet(bot, message, index):
    index_list['wallet'] = int(index)
    result['wallet'] = int(index)
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def select_buy_amount(bot, message, index):
    index_list['buy_amount'] = int(index)
    result['buy_amount'] = chain_buy_amounts[int(index)]
    x_value_list['buy-amount'] = 0
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)

    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def select_slip_page(bot, message, index):

    index_list['slippage'] = int(index)
    #  user_model.update_user_by_id(user.id, 'wallets', user.wallets)
    result['slippage'] = chain_slippages[int(index)]
    x_value_list['slippage'] = 0
    
    image_url = main_api.get_price_chart(result['token'])

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
      *🪁 Swing Trading* >> Manual Mode

  *{meta_data['name']}  (🔗{current_chain})  *
  {token}
      
  💲 *Price:* {token_price}$
  💧 *Liquidity:* {token_liquidity}$
  📊 *Market Cap:* {token_market_cap}$

  [Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
  '''
    keyboard = get_keyboard( x_value_list,
                            message.chat.id, index_list)

    with open(image_url, 'rb') as image:
        bot.send_photo(chat_id=message.chat.id, photo = image, caption=text, parse_mode='Markdown', reply_markup=keyboard)

def handle_select_auto_slippage(bot, message, index):
  text = '''
      *🪁 Swing Trading*
 Do you confirm 50% slippage as Auto Slippage?.
'''
  keyboard = types.InlineKeyboardMarkup()
  cancel = types.InlineKeyboardButton('Cancel', callback_data='manual swing select slippage x')
  confirm = types.InlineKeyboardButton('Confirm', callback_data=f'manual swing confirm select slippage {index}')
  keyboard.row(cancel, confirm)
  bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                    reply_markup=keyboard, disable_web_page_preview=True)
  
def handle_buy_amount_x(bot, message):
    text = '''
*Token Buy > 💰 X*
Enter the amount to buy:
'''
    item = "Buy Amount"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_slippage_x(bot, message):
    text = '''
*Token Buy > 💧 X%*
Enter the slippage to set:
'''
    item = "Slippage"
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_value(bot, next_message, item))

def handle_more_btn(bot, message):
    x_value_list['more_btn_index'] += 1
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
    
def handle_input_value(bot, message, item):
    if item == "Buy Amount":
        buy_amount_x = float(message.text)
        x_value_list['buy-amount'] = buy_amount_x
        result['buy_amount'] = buy_amount_x
        index_list['buy_amount'] = 100
    elif item == "Slippage":
        slippage_x = float(message.text)
        x_value_list['slippage'] = slippage_x
        result['slippage'] = slippage_x
        index_list['slippage'] = 100
    keyboard = get_keyboard(x_value_list,
                            message.chat.id, index_list)
    image_url = main_api.get_price_chart(result['token'])
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
    *🪁 Swing Trading* >> Manual Mode

*{meta_data['name']}  (🔗{current_chain})  *
{token}
    
💲 *Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://solscan.io/account/{token}) | [Dexscreener](https://dexscreener.com/solana/{token}) | [Defined](https://www.defined.fi/sol/{token}?quoteToken=token1&cache=3e1de)
'''
    with open(image_url, 'rb') as image:
        bot.send_photo(chat_id=message.chat.id, photo = image, caption=text, parse_mode='Markdown', reply_markup=keyboard)


def handle_buy(bot, message):
    chain_index = main_api.get_chain(message.chat.id)
    chains = main_api.get_chains()
    wallets = main_api.get_wallets(message.chat.id)
    buy_wallet = wallets[result['wallet']]['id']
    buy_amount = int(result['buy_amount'] * 1_000_000_000)
    bot.send_message(chat_id=message.chat.id,
                     text='Buy Transaction sent. Please take for about 10 seconds to be confirmed')
    position = main_api.market_buy(message.chat.id, result['token'], buy_amount, result['slippage'], buy_wallet, True)
    result_text = f'''Successfully confirmed Buy Transaction.
Transaction ID: {position['transaction_id']}
View on SolScan: (https://solscan.io/tx/{position['transaction_id']})'''
    bot.send_message(chat_id=message.chat.id,
                     text=result_text)