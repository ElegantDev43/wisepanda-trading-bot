from telebot import types

from src.database import user as user_model
from src.engine import main as engine

def handle_hots(bot, message):
    user = user_model.get_user_by_telegram(message.chat.id)
    hot_tokens = engine.get_hot_tokens(user.chain)

    text = f'''
*Hot Tokens*
    '''

    for token in hot_tokens:
        text += f'''
{token['token0']['symbol']}/{token['token1']['symbol']}
'''

    keyboard = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(back)
    keyboard.row(close)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)