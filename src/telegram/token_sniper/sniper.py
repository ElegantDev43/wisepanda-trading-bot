from telebot import types

from src.engine import api as main_api

def handle_sniper(bot, message):
   # user_model.create_user_by_telegram(message.chat.id)
    text = '''
*🎯 Trade New Tokens*

*Auto Mode* - Trade new tokens automatically.
*Manual Mode* - Trade an inputed token with parameters.
*Token Snipers* - Currently ongoing snipers.

    '''

    keyboard = types.InlineKeyboardMarkup()
    auto_mode_btn = types.InlineKeyboardButton(
      text="🎮 Auto Mode", callback_data=f"sniper select auto mode")
    paste_mode_btn = types.InlineKeyboardButton(
      text="🤏 Manual Mode", callback_data=f"sniper select manual mode")
    
    positions = types.InlineKeyboardButton(
        '📊 Token Snipers', callback_data='manage-token-snipers')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(auto_mode_btn, paste_mode_btn, positions)
    keyboard.row(back, close)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
