from telebot import types

from src.database import user as user_model

def handle_positions(bot, message):
    user = user_model.get_user_by_telegram(message.chat.id)

    text = f'''
*Open Positions*

You currently have {len(user.positions)} open positions.

Your positions are:
    '''

    for position in user.positions:
            text += f'''
Chain: {position['chain']}
Token: {position['token']}
Balance: {position['balance']}
            '''

    keyboard = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(back)
    keyboard.row(close)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)