from telebot import types

from src.database import user as user_model
from src.engine import main as engine

def handle_buyer(bot, message):
    user_model.create_user_by_telegram(message.chat.id)

    text = '''
*Manual Buyer*
Paste in a token address below to buy manually
e.g. 0x7169D38820dfd117C3FA1f22a697dBA58d90BA06
    '''

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=lambda next_message: handle_input_token(bot, next_message))

def get_keyboard(user_wallets):
    wallet_count = len(user_wallets)
    buy_amounts = [0.01, 0.02, 0.05, 0.1]
    buy_count = len(buy_amounts)

    keyboard = types.InlineKeyboardMarkup()

    wallets = []
    for index in range(wallet_count):
        wallets.append(types.InlineKeyboardButton(f'W{index + 1}{" 🟢" if user_wallets[index]['active'] == True else ""}', callback_data=f'manual wallet {index}'))
    wallet_all = types.InlineKeyboardButton('All Wallets', callback_data=f'manual wallet all')
    buys = []
    for buy_amount in buy_amounts:
        buys.append(types.InlineKeyboardButton(f'💰 {buy_amount}Ξ', callback_data=f'manual buy {buy_amount}'))
    buy_x = types.InlineKeyboardButton('💰 XΞ', callback_data='manual buy x')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(*wallets[0:(wallet_count // 2)])
    keyboard.row(*wallets[(wallet_count // 2):wallet_count])
    keyboard.row(wallet_all)
    keyboard.row(*buys[0:(buy_count // 2)])
    keyboard.row(*buys[(buy_count // 2):buy_count])
    keyboard.row(buy_x)
    keyboard.row(back, close)

    return keyboard

def handle_input_token(bot, message):
    user = user_model.get_user_by_telegram(message.chat.id)
    chain = user.chain
    token = message.text

    if engine.check_token_liveness(chain, token) == False:
        bot.send_message(chat_id=message.chat.id, text='Error: This is not a live token')
        return

    user_model.update_user_by_id(user.id, 'session', {'token': token})

    name = engine.get_token_name(chain, token)
    exchange_data = engine.get_token_information(chain, token)

    text = f'''
*{name}  (🔗{chain})*
{token}
{exchange_data}

[Scan](https://etherscan.io/address/{token}) | [Dexscreener](https://dexscreener.com/ethereum/{token}) | [DexTools](https://www.dextools.io/app/en/ether/pair-explorer/{token}) | [Defined](https://www.defined.fi/eth/{token})
    '''

    keyboard = get_keyboard(user.wallets[chain])

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)

def handle_toggle_wallet(bot, message, index):
    user = user_model.get_user_by_telegram(message.chat.id)
    chain = user.chain
    wallets = user.wallets[chain]

    if index == 'all':
        active_all = True
        for wallet in wallets:
            if wallet['active'] == False:
                active_all = False
                break

        active = not active_all
        for index in range(len(wallets)):
            wallets[index]['active'] = active
    else:
        index = int(index)
        wallets[index]['active'] = not wallets[index]['active']

    user_model.update_user_by_id(user.id, 'wallets', user.wallets)

    keyboard = get_keyboard(wallets)

    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)

def handle_buy_x(bot, message):
    text = '''
*Manual Buyer > 💰 XΞ*
Enter the amount to buy:
'''

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=lambda next_message: handle_input_buy_x(bot, next_message))

def handle_input_buy_x(bot, message):
    amount = float(message.text)
    handle_buy(bot, message, amount)

def handle_buy(bot, message, amount):
    user = user_model.get_user_by_telegram(message.chat.id)
    chain = user.chain
    wallets = []
    for wallet in user.wallets[chain]:
        if wallet['active'] == True:
            wallets.append(wallet)

    engine.create_order(chain, user.id, user.session['token'], 'market', 'buy', amount, wallets)

    bot.send_message(chat_id=message.chat.id, text='Executed manual buy transaction')
