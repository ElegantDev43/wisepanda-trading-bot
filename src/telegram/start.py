from telebot import types

from src.database import user as user_model


def handle_start(bot, message):
    user_model.create_user_by_telegram(message.chat.id)

    text = '''
*Welcome to the Panda Bot!*

We’re excited to present a revolutionary trading bot designed specifically for the growing popoularity.
With Panda Bot, you can trade any token instantly, taking advantage of market opportunities the moment they appear.
    
💬 [Visit our Official Chat](https://t.me/wisepandaofficial)

🌍 [Visit our Website](https://www.wisepanda.ai)
    '''

    keyboard = types.InlineKeyboardMarkup()
    sniper = types.InlineKeyboardButton(
        '🎯 Token Sniper', callback_data='sniper')
    hots = types.InlineKeyboardButton('🔥 Hot Tokens', callback_data='hots')
    swing = types.InlineKeyboardButton(
        '🪁 Swing Trading', callback_data='swing')
    buyer = types.InlineKeyboardButton('🛒 Buy', callback_data='buyer')
    seller = types.InlineKeyboardButton(
        '💸 Sell', callback_data='seller')
    positions = types.InlineKeyboardButton(
        '📊 Open Positions', callback_data='positions')
    orders = types.InlineKeyboardButton(
        '⏳ Pending Orders', callback_data='manage-pending-orders')
    limit_order = types.InlineKeyboardButton(
        '🚀 Limit Orders', callback_data='manage-limit-orders')
    dca_order = types.InlineKeyboardButton(
        '🕒 DCA Orders', callback_data='manage-dca-orders')
    settings = types.InlineKeyboardButton(
        '🔧 Settings', callback_data='settings')
    bridge = types.InlineKeyboardButton(
        '🌉 Bridge', callback_data='bridges')
    referral = types.InlineKeyboardButton(
        '💰 Referral', callback_data='referrals')
    weekly = types.InlineKeyboardButton(
        '🤚 Weekly Claim', callback_data='weekly-claim')
    copy_trading = types.InlineKeyboardButton(
        '📋 Copy Trading', callback_data='copytrades')
    bots = types.InlineKeyboardButton('🤖 Backup Bots', callback_data='bots')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(sniper, swing)
    keyboard.row(buyer, seller)
    keyboard.row(positions, orders)
    keyboard.row(limit_order, dca_order)
    keyboard.row(copy_trading)
    keyboard.row(bridge, referral, weekly)
    keyboard.row(bots,  hots, settings)
    keyboard.row(close)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
