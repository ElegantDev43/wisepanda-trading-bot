from telebot import types
from src.engine import api as main_api
import sys

def handle_start(bot, message):
    if not main_api.get_user(message.chat.id):
      main_api.add_user(message.chat.id)

    text = '''
*Welcome to the Panda Bot!*

We’re excited to present a revolutionary trading bot designed specifically for the growing popoularity.
With Panda Bot, you can trade any token instantly, taking advantage of market opportunities the moment they appear.
    
    '''

    keyboard = types.InlineKeyboardMarkup()
    sniper = types.InlineKeyboardButton(
        '🎯 Trade New Tokens', callback_data='sniper')
    lp_sniper = types.InlineKeyboardButton(
        '🔫 LP Sniper', callback_data='lp sniper')
    hots = types.InlineKeyboardButton('🔥 Hot Tokens', callback_data='hots')
    swing = types.InlineKeyboardButton(
        '🪁 Swing Trading', callback_data='swing')
    buyer = types.InlineKeyboardButton('🛒 Buy', callback_data='buyer')
    seller = types.InlineKeyboardButton(
        '💸 Sell', callback_data='seller')
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
    anom_trading = types.InlineKeyboardButton(
        '🕵️‍♂️ Anonymous Trading', callback_data='anonym-trade')
    help_doc = types.InlineKeyboardButton(
        '📓 Help', url=f'https://t.me/wisepandaofficial')
    official_chat = types.InlineKeyboardButton(
        '🌍 Official Chat', url=f'https://t.me/wisepandaofficial')
    bots = types.InlineKeyboardButton('🤖 Backup Bots', callback_data='bots')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(sniper, lp_sniper, swing)
    keyboard.row(copy_trading, anom_trading)
    keyboard.row(buyer, seller)
    keyboard.row(limit_order, dca_order)
    keyboard.row(bridge, referral, weekly)
    keyboard.row(bots,  settings)
    keyboard.row(help_doc, official_chat)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
