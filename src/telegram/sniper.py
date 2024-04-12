from telebot import types

from src.database import user as user_model

from telebot import types

from src.database import user as user_model
from src.engine import main as engine

def handle_auto_sniper_or_manual_buyer(bot, message):
    user_model.create_user(message.chat.id)

    text = '''
*Auto Sniper / Manual Buyer*
Paste in a token address below to start buying
e.g. 0x6982508145454Ce325dDbE47a25d4ec3d2311933
    '''

    bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=lambda next_message: handle_input_token(bot, next_message))

def handle_input_token(bot, message):
    user = user_model.get_user(message.chat.id)
    user_chain = user.chain

    token = message.text
    token_chain = engine.get_token_chain(token)

    if token_chain == None:
        bot.send_message(chat_id=message.chat.id, text='Invalid token address')
        return

    if user_chain != token_chain:
        user_model.update_user(user.id, 'chain', token_chain)

    if engine.get_token_information(token) == None:
        sniper.handle_auto_sniper(bot, message)
    else:
        buyer.handle_manual_buyer(bot, message)


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
