from telebot import types

from src.database import user as user_model

def handle_start(bot, message):
    user_model.create_user(message.chat.id)

    text = '''
*Wise Panda 1.0*
The fastest and sleekest trading bot

📖 [Visit our Website](https://docs.wisepanda.ai)
💬 [Visit our Official Chat](https://t.me/wisepandaofficial)
🌍 [Visit our Website](https://www.wisepanda.ai)

*Paste a contract address or pick an option to get started.*
    '''

    keyboard = types.InlineKeyboardMarkup()
    auto_sniper = types.InlineKeyboardButton('🎯 Auto Sniper', callback_data='auto_sniper')
    manual_buyer = types.InlineKeyboardButton('🤏 Manual Buyer', callback_data='manual_buyer')
    orders = types.InlineKeyboardButton('🕐 Pending Orders', callback_data='orders')
    positions = types.InlineKeyboardButton('📊 Open Positions', callback_data='positions')
    copy_trading = types.InlineKeyboardButton('🕵 Copy Trading', callback_data='copy_trading')
    settings = types.InlineKeyboardButton('🔧 Settings', callback_data='settings')
    refer = types.InlineKeyboardButton('💲 Refer & Earn', callback_data='refer')
    bots = types.InlineKeyboardButton('🤖 Backup Bots', callback_data='bots')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(auto_sniper, manual_buyer)
    keyboard.row(orders, positions)
    keyboard.row(copy_trading, settings)
    keyboard.row(refer, bots)
    keyboard.row(close)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)