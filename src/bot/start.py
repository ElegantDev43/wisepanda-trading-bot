from telebot import types

from src import database

def handle_start(bot, message):
    database.create_user(message.chat.id)

    text = '''
*Welcome to Wise Panda Trading Bot!*

[Visit our Official Chat](https://t.me/wisepandaofficial)

[Visit our Website](https://www.wisepanda.ai)
    '''

    keyboard = types.InlineKeyboardMarkup()
    auto_sniper = types.InlineKeyboardButton('Auto Sniper', callback_data='auto_sniper')
    manual_buyer = types.InlineKeyboardButton('Manual Buyer', callback_data='manual_buyer')
    orders = types.InlineKeyboardButton('Pending Orders', callback_data='orders')
    positions = types.InlineKeyboardButton('Open Positions', callback_data='positions')
    copy_trading = types.InlineKeyboardButton('Copy Trading', callback_data='copy_trading')
    settings = types.InlineKeyboardButton('Settings', callback_data='settings')
    refer = types.InlineKeyboardButton('Refer & Earn', callback_data='refer')
    bots = types.InlineKeyboardButton('Backup Bots', callback_data='bots')
    keyboard.row(auto_sniper, manual_buyer)
    keyboard.row(orders, positions)
    keyboard.row(copy_trading, settings)
    keyboard.row(refer, bots)

    bot.send_message(message.chat.id, text, parse_mode='Markdown', disable_web_page_preview=True, reply_markup=keyboard)
