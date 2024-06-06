from telebot import types

#from src.database import user as user_model
#from src.engine import main as engine
from src.database import swing as swing_model
from src.telegram.start import handle_start

buy_amounts = [0.1, 0.3, 0.5, 1]
trade_durations = [7,14,30]

default_duration = 14
default_amount = 0.1
default_buy_index = 0

def handle_token_selection(bot, message):
    #user_model.create_user_by_telegram(message.chat.id)

    text = '''
*Auto Sniper*
Paste in a token address below to setup auto sniper for new launching token.
e.g. 0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7
    '''

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=lambda next_message: handle_autoorder(bot, next_message))

def get_keyboard(wallet_index , buy_index , buyer_amount,trade_duration):

    
    buy_count = len(buy_amounts)
    
    keyboard = types.InlineKeyboardMarkup()

    buys = []
    for index in range(0,buy_count):
        buys.append(types.InlineKeyboardButton(f'{"🟢 " if buy_index == index else ""}💰 {buy_amounts[index]}', callback_data=f'auto_buy {index}'))
    buy_x = types.InlineKeyboardButton(f'{"🟢 " if buy_index == 4 else ""}💰 X', callback_data='auto_buy 4')

    buy = types.InlineKeyboardButton('▶️  Start', callback_data='auto_start')
    period = types.InlineKeyboardButton(f'🕒️ Durations ({trade_duration})', callback_data='auto_period')
    token_wallet = types.InlineKeyboardButton('💳 Wallet', callback_data='token_wallet')
    amounts = types.InlineKeyboardButton(f'💰️ Buy Amounts ({buyer_amount})', callback_data='amounts')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='swing')

    keyboard.row(buy)
    keyboard.row(period,token_wallet)
    keyboard.row(amounts)
    keyboard.row(*buys[0:(buy_count // 2)])
    keyboard.row(*buys[(buy_count // 2):buy_count],buy_x)
    keyboard.row(back)

    return keyboard


def handle_autoorder(bot, message):

    # user_model.create_user_by_telegram(message.chat.id)
    global default_duration,default_amount,default_buy_index
    token = 'So11111111111111111111111111111111111111112'

    image_path = f'src/engine/swing/data_png/prices_{token}.png'  # Local image file path

    chain = 'ethereum'

    name = "elo"

    text = f'''
*{name}  (🔗{chain})*
{token}

[Scan](https://etherscan.io/address/{token}) | [Dexscreener](https://dexscreener.com/ethereum/{token}) | [DexTools](https://www.dextools.io/app/en/ether/pair-explorer/{token}) | [Defined](https://www.defined.fi/eth/{token})
    '''

    keyboard = get_keyboard(0,default_buy_index,default_amount,default_duration)

    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    with open(image_path, 'rb') as image:
        bot.send_photo(chat_id=message.chat.id, photo = image, caption=text, parse_mode='Markdown', reply_markup=keyboard)
        #bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)


def handle_toggle(bot, message,type, index,amounts,duration):

    global default_duration,default_amount,default_buy_index

    if type == 'toggle_buy':
        buyer_amount = 0
        if index < 4:
            buyer_amount = buy_amounts[index]

        elif index == 4:
            buyer_amount = amounts

        default_buy_index = index
        default_amount = buyer_amount
    elif type == 'toggle_duration':
        default_duration = duration

    keyboard = get_keyboard(0,default_buy_index,default_amount,default_duration)
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
    handle_toggle(bot, prev_message,'toggle_buy', 4,amount,default_duration)

def handle_duration_x(bot, message):
    text = '''
*Auto Order > 🕒️ Durations*
Enter the duration for trading:
'''

    new_message = bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=lambda next_message: handle_input_duration_x(bot, next_message,message,new_message))

def handle_input_duration_x(bot, message,prev_message,new_message):
    amount = int(message.text)
    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.delete_message(chat_id = message.chat.id, message_id = new_message.message_id, timeout = 0 )
    handle_toggle(bot, prev_message,'toggle_duration', default_buy_index,default_amount,amount)


def handle_autostart(bot, message):
  swing_model.add_by_user_id(1,'solana','0x0EDc58C57Fc5e7D441484bffb5750eA4dFacBa8C',
                             default_duration,default_amount,'0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7')

  bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
  handle_start(bot, message)