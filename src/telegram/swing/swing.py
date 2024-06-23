from telebot import types

from src.database.swing import Htokens as HTokens_model

def handle_start(bot, message):

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
    trade_history = types.InlineKeyboardButton('📊 Manage Tokens', callback_data='trade_history')
    swing_position = types.InlineKeyboardButton('📊 Open Positions', callback_data='swing_positions')

    keyboard.row(auto_token,select_token)
    keyboard.row(manual_swing,swing_position)
    keyboard.row(trade_history,back)

    #bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)