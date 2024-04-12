from telebot import types

from src.database import user as user_model

def handle_auto_sniper(bot, chat_id, token):
    text = f'''
*New Token  (🔗{token['chain']})*
{token['address']}
❌ Snipe not set

Scan (https://etherscan.io/address/{token['address']}) | Dexscreener (https://dexscreener.com/ethereum/{token['address']}) | DexTools (https://www.dextools.io/app/en/ether/pair-explorer/{token['address']}) | Defined (https://www.defined.fi/eth/{token['address']})
    '''

    buy_amounts = [0.01, 0.02, 0.05, 0.1]

    keyboard = types.InlineKeyboardMarkup()
    for buy_amount in buy_amounts:
        buy_button = types.InlineKeyboardButton(f'💰 {buy_amount}Ξ', callback_data='close')
        keyboard.add(buy_button)

    buy_x_button = types.InlineKeyboardButton('💰 XΞ', callback_data='close')
    keyboard.row(buy_x_button)

    bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown', reply_markup=keyboard)
