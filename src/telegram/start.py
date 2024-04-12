from telebot import types

from src.database import user as user_model

def handle_start(bot, message):
    user_model.create_user_with_telegram(message.chat.id)

    text = '''
*Panda 1.0*
The fastest and sleekest trading bot the cryptosphere has seen

💬 [Visit our Official Chat](https://t.me/wisepandaofficial)

🌍 [Visit our Website](https://www.wisepanda.ai)
    '''

    keyboard = types.InlineKeyboardMarkup()
    auto_sniper = types.InlineKeyboardButton('🎯 Auto Sniper', callback_data='auto_sniper')
    manual_buyer = types.InlineKeyboardButton('🤏 Manual Buyer', callback_data='manual_buyer')
    orders = types.InlineKeyboardButton('🕐 Pending Orders', callback_data='orders')
    positions = types.InlineKeyboardButton('📊 Open Positions', callback_data='positions')
    settings = types.InlineKeyboardButton('🔧 Settings', callback_data='settings')
    bots = types.InlineKeyboardButton('🤖 Backup Bots', callback_data='bots')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(auto_sniper, manual_buyer)
    keyboard.row(orders, positions)
    keyboard.row(settings, bots)
    keyboard.row(close)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)