from telebot import types

from src.database import user as user_model

def handle_start(bot, message):
    user_model.create_user_by_telegram(message.chat.id)

    text = '''
*Panda 1.0*
The fastest and sleekest trading bot the cryptosphere has ever seen.

💬 [Visit our Official Chat](https://t.me/wisepandaofficial)

🌍 [Visit our Website](https://www.wisepanda.ai)
    '''

    keyboard = types.InlineKeyboardMarkup()
    sniper = types.InlineKeyboardButton('🎯 Auto Sniper', callback_data='sniper')
    hots = types.InlineKeyboardButton('🔥 Hot Tokens', callback_data='hots')
    buyer = types.InlineKeyboardButton('🤏 Manual Buyer', callback_data='buyer')
    positions = types.InlineKeyboardButton('📊 Open Positions', callback_data='positions')
    orders = types.InlineKeyboardButton('🕐 Pending Orders', callback_data='orders')
    settings = types.InlineKeyboardButton('🔧 Settings', callback_data='settings')
    bots = types.InlineKeyboardButton('🤖 Backup Bots', callback_data='bots')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(sniper, hots)
    keyboard.row(buyer, positions)
    keyboard.row(orders, settings)
    keyboard.row(bots, close)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)