from telebot import types

from src.database import user as user_model
from src.engine import main as engine

def handle_hots(bot, message):
    user = user_model.get_user_by_telegram(message.chat.id)
    hot_tokens = engine.get_hot_tokens(user.chain)

    text = f'''
*Hot Tokens*

The following tokens are the hotest ones on {user.chain} recently.
Click one of them to start to buy manually.
    '''

    keyboard = types.InlineKeyboardMarkup()
    for token in hot_tokens:
        button = types.InlineKeyboardButton(token['token0']['symbol'], callback_data=f'hot {token['token0']['id']}')
        keyboard.row(button)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(back)
    keyboard.row(close)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)