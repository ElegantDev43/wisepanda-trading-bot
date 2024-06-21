from telebot import types

from src.database.swing import Htokens as HTokens_model

def handle_start(bot, message):
    limit = 2
    sh_bul_tokens,sh_bea_tokens,me_bul_tokens,me_bea_tokens,lo_bul_tokens,lo_bea_tokens = HTokens_model.get_hot_tokens(limit)

    # hot_bearish_tokens = ['A','B','C','D','E','F']
    # hot_bullish_tokens = ['G','H','I','J','K','L']
    bearish_buttons = []
    bullish_buttons = []

    token_count = len(sh_bul_tokens)

    for index in range(token_count):
        bearish_buttons.append(types.InlineKeyboardButton(sh_bea_tokens[index].name, callback_data=f'auto_token_{sh_bea_tokens[index].address}'))
        bullish_buttons.append(types.InlineKeyboardButton(sh_bul_tokens[index].name, callback_data=f'auto_token_{sh_bul_tokens[index].address}'))

    for index in range(token_count):
        bearish_buttons.append(types.InlineKeyboardButton(me_bea_tokens[index].name, callback_data=f'auto_token_{me_bea_tokens[index].address}'))
        bullish_buttons.append(types.InlineKeyboardButton(me_bul_tokens[index].name, callback_data=f'auto_token_{me_bul_tokens[index].address}'))

    for index in range(token_count):
        bearish_buttons.append(types.InlineKeyboardButton(lo_bea_tokens[index].name, callback_data=f'auto_token_{lo_bea_tokens[index].address}'))
        bullish_buttons.append(types.InlineKeyboardButton(lo_bul_tokens[index].name, callback_data=f'auto_token_{lo_bul_tokens[index].address}'))

    text = '''
*Welcome to Swing Trading!*
Discover and engage with the newest tokens as they launch. Gain a competitive edge with early investment opportunities.

💬 [Visit our Official Chat](https://t.me/wisepandaofficial)

🌍 [Visit our Website](https://www.wisepanda.ai)
    '''

    keyboard = types.InlineKeyboardMarkup()
    short_bearish_tokens = types.InlineKeyboardButton('📉 Short Bearish Tokens', callback_data='Default')
    medium_bearish_tokens = types.InlineKeyboardButton('📉 Medium Bearish Tokens', callback_data='Default')
    long_bearish_tokens = types.InlineKeyboardButton('📉 Long Bearish Tokens', callback_data='Default')
    short_bullish_tokens = types.InlineKeyboardButton('📈 Short Bullish Tokens', callback_data='Default')
    medium_bullish_tokens = types.InlineKeyboardButton('📈 Medium Bullish Tokens', callback_data='Default')
    long_bullish_tokens = types.InlineKeyboardButton('📈 Long Bullish Tokens', callback_data='Default')
    select_token = types.InlineKeyboardButton('🤏 Select Token', callback_data='select_token')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    trade_history = types.InlineKeyboardButton('📊 Trade History', callback_data='trade_history')
    keyboard.row(short_bearish_tokens, short_bullish_tokens)
    keyboard.row(bearish_buttons[0],bearish_buttons[1],bullish_buttons[0],bullish_buttons[1])
    keyboard.row(medium_bearish_tokens, medium_bullish_tokens)
    keyboard.row(bearish_buttons[2],bearish_buttons[3],bullish_buttons[2],bullish_buttons[3])
    keyboard.row(long_bearish_tokens, long_bullish_tokens)
    keyboard.row(bearish_buttons[4],bearish_buttons[5],bullish_buttons[4],bullish_buttons[5])
    keyboard.row(select_token)
    keyboard.row(trade_history,back)

    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)