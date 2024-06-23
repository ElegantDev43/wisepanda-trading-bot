import os
import asyncio
from telebot import types

#from src.database import user as user_model
#from src.engine import main as engine
from src.engine.swing.data_extract import exportTestValues
from src.engine import api as main_api

from src.database.swing import swing as swing_model
from src.database.swing import Htokens as htokens_model
from src.database import user as user_model

from src.telegram.start import handle_start

buy_amounts = [100]
trade_slips = [10,30,50]

default_slip = 30
default_amount = 100
default_buy_index = 0
default_wallet_index = 0
default_token_address = ''

chain_name = ['solana','ethereum']

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

def handle_token_selection(bot, message):
    #user_model.create_user_by_telegram(message.chat.id)

    text = '''
*Auto Trading*
Paste in a token address below to setup auto sniper for new launching token.
e.g. 5oVNBeEEQvYi1cX3ir8Dx5n1P7pdxydbGF2X4TxVusJm
    '''

    new_message = bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=lambda next_message: handle_input_address_x(bot, next_message,message,new_message))

def handle_input_address_x(bot, message,prev_message,new_message):
    address = message.text
    # bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    # bot.delete_message(chat_id = message.chat.id, message_id = new_message.message_id, timeout = 0 )
    handle_autoorder(bot, prev_message,address)

def set_auto_address(bot,message):
  address = htokens_model.get_top_hot_token()
  handle_autoorder(bot,message,address)

def get_keyboard(message,wallet_index , buy_index , buyer_amount,trade_slip):
    user = user_model.get(message.chat.id)
    chain = user.chain
    wallets = user.wallets[chain]

    buy_count = len(buy_amounts)
    wallet_count = len(wallets)

    keyboard = types.InlineKeyboardMarkup()

    buys = []
    for index in range(0,buy_count):
        buys.append(types.InlineKeyboardButton(f'{"🟢 " if buy_index == index else ""}💰 {buy_amounts[index]}', callback_data=f'auto_buy {index}'))
    buy_x = types.InlineKeyboardButton(f'{"🟢 " if buy_index == 4 else ""}💰 {"X" if buyer_amount == 100 else f'{buyer_amount}'}', callback_data='auto_buy 4')

    btn_wallets = []
    for index in range(wallet_count):
        btn_wallets.append(types.InlineKeyboardButton(f'{"🟢 " if wallet_index == index else ""} W{index + 1}', callback_data=f'auto_wallet {index}'))

    buy = types.InlineKeyboardButton('▶️  Start', callback_data='auto_start')
    #slip = types.InlineKeyboardButton(f'📉 Slip ({trade_slip})', callback_data='auto_slip')
    token_wallet = types.InlineKeyboardButton('💳 Wallet', callback_data='token_wallet')
    wallet_expand = types.InlineKeyboardButton('Expand', callback_data='token_wallet_expand')
    amounts = types.InlineKeyboardButton(f'Buy :', callback_data='Default')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='swing')

    keyboard.row(buy)
    #keyboard.row(slip)
    if wallet_count < 3:
      keyboard.row(*btn_wallets[0:wallet_count])
    elif wallet_count >= 4:
      keyboard.row(*btn_wallets[0:2],wallet_expand)
    keyboard.row(amounts,*buys,buy_x)
    keyboard.row(back)

    return keyboard


def handle_autoorder(bot, message, address):

    # user_model.create_user_by_telegram(message.chat.id)
    global default_slip,default_amount,default_buy_index,default_wallet_index,default_token_address
    if os.path.exists(f'src/engine/swing/data_png/prices_{address}.png') != True:
        asyncio.run(exportTestValues(address))

    image_path = f'src/engine/swing/data_png/prices_{address}.png'  # Local image file path
    default_token_address = address

    user = user_model.get(message.chat.id)
    chain = user.chain
    wallets = user.wallets[chain]
    walletinfo = ''
    # for index in range(0,len(wallets)):
    #     if index > 0:
    #         walletinfo += '|'
    #     walletinfo += f'W{index + 1}: {wallets[index]['balance']:.3f}Ξ'

#    token = 0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7
    token = address

#    chain = 'ethereum'

#    name = "elo"
    name = htokens_model.get_token_name_by_address(address)

    token_data = main_api.get_token_market_data(message.chat.id, token)
    meta_data = main_api.get_token_metadata(message.chat.id, token)
    
    token_price = format_number(token_data['price'])
    token_liquidity = format_number(token_data['liquidity'])
    token_market_cap = format_number(token_data['market_cap'])

    text = f'''
*{name}  (🔗{chain_name[chain]})*
{token}

💲 *Price:* {token_price}$
💧 *Liquidity:* {token_liquidity}$
📊 *Market Cap:* {token_market_cap}$

[Scan](https://etherscan.io/address/{token}) | [Dexscreener](https://dexscreener.com/ethereum/{token}) | [DexTools](https://www.dextools.io/app/en/ether/pair-explorer/{token}) | [Defined](https://www.defined.fi/eth/{token})
    '''

    keyboard = get_keyboard(message,0,default_buy_index,default_amount,default_slip)

    # bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    with open(image_path, 'rb') as image:
        bot.send_photo(chat_id=message.chat.id, photo = image, caption=text, parse_mode='Markdown', reply_markup=keyboard)
        #bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)


def handle_toggle(bot, message,type,wallet_index, index,amounts,slip):

    global default_slip,default_amount,default_buy_index,default_wallet_index

    if type == 'toggle_buy':
        buyer_amount = 0
        if index < 4:
            buyer_amount = buy_amounts[index]

        elif index == 4:
            buyer_amount = amounts

        default_buy_index = index
        default_amount = buyer_amount
    elif type == 'toggle_slip':
        default_slip = slip
    elif type == 'toggle_wallet':
        default_wallet_index = wallet_index

    keyboard = get_keyboard(message,default_wallet_index,default_buy_index,default_amount,default_slip)
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def handle_buy_x(bot, message):
    text = '''
*Auto Order > 💰 X*
Enter the amount to buy:
'''

    new_message = bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=lambda next_message: handle_input_buy_x(bot, next_message,message,new_message))

def handle_input_buy_x(bot, message,prev_message,new_message):
    amount = float(message.text)
    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.delete_message(chat_id = message.chat.id, message_id = new_message.message_id, timeout = 0 )
    handle_toggle(bot, prev_message,'toggle_buy',0, 4,amount,default_slip)

def handle_slip_x(bot, message):
    text = '''
*Auto Order > 📉 Slippage*
🛴 Enter the slippage amount:
'''

    new_message = bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=lambda next_message: handle_input_slip_x(bot, next_message,message,new_message))

def handle_input_slip_x(bot, message,prev_message,new_message):
    amount = int(message.text)
    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.delete_message(chat_id = message.chat.id, message_id = new_message.message_id, timeout = 0 )
    handle_toggle(bot, prev_message,'toggle_slip',0, default_buy_index,default_amount,amount)


def handle_autostart(bot, message):
  global default_token_address

  user = user_model.get(message.chat.id)
  chain = user.chain
  wallets = user.wallets[chain]

  swing_model.add_by_user_id(message.chat.id,'solana',wallets[default_wallet_index],
                             default_slip,default_amount,default_token_address)

  # bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
  handle_start(bot, message)