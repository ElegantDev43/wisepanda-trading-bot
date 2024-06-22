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
🪁 🪁 🪁
Discover and engage with the newest tokens as they launch. Gain a competitive edge with early investment opportunities.

💬 [Visit our Official Chat](https://t.me/wisepandaofficial)

🌍 [Visit our Website](https://www.wisepanda.ai)
    '''

    keyboard = types.InlineKeyboardMarkup()
    auto_token = types.InlineKeyboardButton('🤖 Auto Swing Trade', callback_data='auto_token')
    select_token = types.InlineKeyboardButton('🤏 Select Token', callback_data='select_token')
    manual_swing = types.InlineKeyboardButton('📋 Manual Trade', callback_data='manual_swing')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    trade_history = types.InlineKeyboardButton('📊 Trade History', callback_data='trade_history')

    keyboard.row(auto_token)
    keyboard.row(select_token)
    keyboard.row(manual_swing)
    keyboard.row(trade_history,back)

    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)