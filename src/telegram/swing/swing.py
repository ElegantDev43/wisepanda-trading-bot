from telebot import types

from src.database.swing import Htokens as HTokens_model

def handle_start(bot, message):

    text = '''
*🪁 Swing Trading*

Discover and engage with the newest tokens as they launch. Gain a competitive edge with early investment opportunities.

Select mode for swing trading.
    '''

    keyboard = types.InlineKeyboardMarkup()
    auto_token = types.InlineKeyboardButton('🤖 Auto Mode', callback_data='swing mode auto')
    select_token = types.InlineKeyboardButton('🤏 Select Token Mode', callback_data='swing mode select_token')
    manual_swing = types.InlineKeyboardButton('📋 Manual Mode', callback_data='swing mode manual')

    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    
    keyboard.row(auto_token, select_token, manual_swing)
    keyboard.row(back, close)
    #bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)