from telebot import types

from src.database import user as user_model

from telebot import types

import config
from src.database import user as user_model
from src.engine import main as engine

def handle_sniper(bot, message):
    user_model.create_user_with_telegram(message.chat.id)

    text = '''
*Auto Sniper*
Paste in a token address below to setup auto sniper for new launching token
e.g. 0x7169D38820dfd117C3FA1f22a697dBA58d90BA06
    '''

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=lambda next_message: handle_input_token(bot, next_message))

def handle_input_token(bot, message):
    user = user_model.get_user_by_telegram(message.chat.id)
    chain = user.chain
    address = message.text
    token = {'chain': chain, 'address': address}

    if engine.check_token_liveness(token) == True:
        bot.send_message(chat_id=message.chat.id, text='Error: This is a live token')
        return

    name = engine.get_token_name(token)

    text = f'''
*{name}  (🔗{chain})*
{address}
❌ Snipe not set

[Scan](https://etherscan.io/address/{address}) | [Dexscreener](https://dexscreener.com/ethereum/{address}) | [DexTools](https://www.dextools.io/app/en/ether/pair-explorer/{address}) | [Defined](https://www.defined.fi/eth/{address})
    '''

    buy_amounts = [0.01, 0.02, 0.05, 0.1]

    keyboard = types.InlineKeyboardMarkup()
    buys = []
    for buy_amount in buy_amounts:
        buys.append(types.InlineKeyboardButton(f'💰 {buy_amount}Ξ', callback_data=f'auto buy {buy_amount}'))
    buy_x = types.InlineKeyboardButton('💰 XΞ', callback_data='auto buy x')
    wallets = []
    for index in range(config.WALLET_COUNT):
        wallets.append(types.InlineKeyboardButton(f'W{index + 1}{" 🟢" if index == 0 else ""}', callback_data=f'auto wallet {index}'))
    wallet_all = types.InlineKeyboardButton('All', callback_data=f'auto wallet all')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(buys[0], buys[1])
    keyboard.row(buys[2], buys[3])
    keyboard.row(buy_x)
    keyboard.row(wallets[0], wallets[1], wallets[2], wallets[3], wallets[4])
    keyboard.row(wallets[5], wallets[6], wallets[7], wallets[8], wallets[9], wallet_all)
    keyboard.row(back, close)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)
