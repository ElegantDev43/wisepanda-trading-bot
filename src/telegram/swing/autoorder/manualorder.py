import os
import asyncio
from telebot import types

#from src.database import user as user_model
#from src.engine import main as engine
from src.engine.swing.data_extract import exportTestValues
from src.database.swing import swing as swing_model
from src.database.swing import Htokens as htokens_model
from src.database import user as user_model
from src.telegram.start import handle_start

buy_amounts = [100, 300, 500, 1000]
sell_amounts = [25, 50, 75, 100]
trade_slips = [10,30,50]


default_slip = 30
default_amount = 100
default_sell_amount = 50
default_buy_index = 0
default_sell_index = 0
default_wallet_index = 0
default_token_address = ''

chain_name = ['solana','ethereum']

def handle_token_selection(bot, message):
    #user_model.create_user_by_telegram(message.chat.id)

    text = '''
*Manual Trading*
Paste in a token address below to setup manual sniper for new launching token.
e.g. 5oVNBeEEQvYi1cX3ir8Dx5n1P7pdxydbGF2X4TxVusJm
    '''

    new_message = bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=lambda next_message: handle_input_address_x(bot, next_message,message,new_message))

def handle_input_address_x(bot, message,prev_message,new_message):
    address = message.text
    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.delete_message(chat_id = message.chat.id, message_id = new_message.message_id, timeout = 0 )
    handle_manual_order(bot, prev_message,address)

def set_manual_address(bot,message):
  address = htokens_model.get_top_hot_token()
  handle_manual_order(bot,message,address)

def get_keyboard(message,wallet_index , buy_index , sell_index, buyer_amount,seller_amount,trade_slip):
  global buy_amounts, sell_amounts
  
  user = user_model.get(message.chat.id)
  chain = user.chain
  wallets = user.wallets[chain]

  buy_count = len(buy_amounts)
  sell_count = len(sell_amounts)
  wallet_count = len(wallets)

  keyboard = types.InlineKeyboardMarkup()

  buys = []
  for index in range(0,buy_count):
      buys.append(types.InlineKeyboardButton(f'{"🟢 " if buy_index == index else ""}💰 {buy_amounts[index]}', callback_data=f'manual_buy {index}'))
  buy_x = types.InlineKeyboardButton(f'{"🟢 " if buy_index == 4 else ""}💰 X', callback_data='manual_buy 4')

  sells = []
  for index in range(0,sell_count):
      sells.append(types.InlineKeyboardButton(f'{"🟢 " if sell_index == index else ""}💰 {sell_amounts[index]}%', callback_data=f'manual_sell {index}'))
  sell_x = types.InlineKeyboardButton(f'{"🟢 " if sell_index == 4 else ""}💰 X%', callback_data='manual_sell 4')

  btn_wallets = []
  for index in range(wallet_count):
      btn_wallets.append(types.InlineKeyboardButton(f'{"🟢 " if wallet_index == index else ""} W{index + 1}', callback_data=f'manual_wallet {index}'))

  # buy = types.InlineKeyboardButton('▶️  Start', callback_data='manual_start')
  slip = types.InlineKeyboardButton(f'📉 Slip ({trade_slip}%)', callback_data='manual_slip')
  token_wallet = types.InlineKeyboardButton('💳 Wallet', callback_data='token_wallet')
  buy_btn = types.InlineKeyboardButton(f'✔️ Buy ({buyer_amount})', callback_data='manual_amounts_buy')
  sell_btn = types.InlineKeyboardButton(f'✔️ Sell ({seller_amount}%)', callback_data='manual_amounts_sell')
  back = types.InlineKeyboardButton('🔙 Back', callback_data='swing')

  # keyboard.row(buy)
  keyboard.row(slip)
  keyboard.row(token_wallet,*btn_wallets[0:(wallet_count // 2)])
  keyboard.row(*btn_wallets[(wallet_count // 2):wallet_count])
  keyboard.row(buy_btn)
  keyboard.row(*buys[0:(buy_count // 2)])
  keyboard.row(*buys[(buy_count // 2):buy_count],buy_x)
  keyboard.row(sell_btn)
  keyboard.row(*sells[0:(sell_count // 2)])
  keyboard.row(*sells[(sell_count // 2):sell_count],sell_x)
  keyboard.row(back)

  return keyboard


def handle_manual_order(bot, message, address):

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


    text = f'''
*{name}  (🔗{chain_name[chain]})*
{token}

[Scan](https://etherscan.io/address/{token}) | [Dexscreener](https://dexscreener.com/ethereum/{token}) | [DexTools](https://www.dextools.io/app/en/ether/pair-explorer/{token}) | [Defined](https://www.defined.fi/eth/{token})
    '''

    keyboard = get_keyboard(message,0,default_buy_index,default_sell_index,default_amount,default_sell_amount,default_slip)

    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    with open(image_path, 'rb') as image:
        bot.send_photo(chat_id=message.chat.id, photo = image, caption=text, parse_mode='Markdown', reply_markup=keyboard)
        #bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)


def handle_toggle(bot, message,type,wallet_index, index,amounts,slip):

    global default_slip,default_amount,default_sell_amount,default_buy_index,default_sell_index,default_wallet_index

    if type == 'toggle_buy':
        buyer_amount = 0
        if index < 4:
            buyer_amount = buy_amounts[index]

        elif index == 4:
            buyer_amount = amounts

        default_buy_index = index
        default_amount = buyer_amount
    elif type == 'toggle_sell':
        seller_amount = 0
        if index < 4:
            seller_amount = sell_amounts[index]

        elif index == 4:
            seller_amount = amounts

        default_sell_index = index
        default_sell_amount = seller_amount
    elif type == 'toggle_slip':
        default_slip = slip
    elif type == 'toggle_wallet':
        default_wallet_index = wallet_index

    keyboard = get_keyboard(message,default_wallet_index,default_buy_index,default_sell_index,default_amount,default_sell_amount,default_slip)
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def handle_buy_x(bot, message):
    text = '''
*manual Order > 💰 X*
Enter the amount to buy:
'''

    new_message = bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=lambda next_message: handle_input_buy_x(bot, next_message,message,new_message))

def handle_input_buy_x(bot, message,prev_message,new_message):
    amount = float(message.text)
    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.delete_message(chat_id = message.chat.id, message_id = new_message.message_id, timeout = 0 )
    handle_toggle(bot, prev_message,'toggle_buy',0, 4,amount,default_slip)


def handle_sell_x(bot, message):
    text = '''
*manual Order > 💰 X*
Enter the amount to sell:
'''

    new_message = bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=lambda next_message: handle_input_sell_x(bot, next_message,message,new_message))

def handle_input_sell_x(bot, message,prev_message,new_message):
    amount = float(message.text)
    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.delete_message(chat_id = message.chat.id, message_id = new_message.message_id, timeout = 0 )
    handle_toggle(bot, prev_message,'toggle_sell',0, 4,amount,default_slip)


def handle_slip_x(bot, message):
    text = '''
*Manual Order > 📉 Slippage*
🛴 Enter the slippage amount:
'''

    new_message = bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=lambda next_message: handle_input_slip_x(bot, next_message,message,new_message))

def handle_input_slip_x(bot, message,prev_message,new_message):
    amount = int(message.text)
    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.delete_message(chat_id = message.chat.id, message_id = new_message.message_id, timeout = 0 )
    handle_toggle(bot, prev_message,'toggle_slip',0, default_buy_index,default_amount,amount)


def handle_manualstart(bot, message):
  global default_token_address

  user = user_model.get(message.chat.id)
  chain = user.chain
  wallets = user.wallets[chain]

  swing_model.add_by_user_id(message.chat.id,'solana',wallets[default_wallet_index]['address'],
                             default_slip,default_amount,default_token_address)

  bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
  handle_start(bot, message)
  
def handle_buy(bot, message):
  user = user_model.get(message.chat.id)
  chain = user.chain
  wallets = user.wallets[chain]
  
#  swap('buy',default_token_address,default_amount,default_slip * 1.0 / 100 , wallets[default_wallet_index])

def handle_sell(bot, message):
  user = user_model.get(message.chat.id)
  chain = user.chain
  wallets = user.wallets[chain]
  
#  swap('sell',default_token_address,default_sell_amount,default_slip * 1.0 / 100 , wallets[default_wallet_index])