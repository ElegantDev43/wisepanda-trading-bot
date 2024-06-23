from telebot import types

from src.database import user as user_model
from src.engine import api as main_api
import threading

def handle_lp_sniper(bot, message):
   # user_model.create_user_by_telegram(message.chat.id)
    text = '''
*🎯 LP Sniper*

Introducing our LP Sniper function: a powerful tool designed
to automatically and accurately snipe liquidity pools,
providing you with the best entry points to maximize your
trading efficiency and returns.
    '''

    keyboard = types.InlineKeyboardMarkup()
    
    auto_mode_btn = types.InlineKeyboardButton(
      text="🎮 Auto Mode", callback_data=f"lp sniper select auto mode")
    paste_mode_btn = types.InlineKeyboardButton(
      text="🤏 Manual Mode", callback_data=f"lp sniper select manual mode")
    
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    
    keyboard.row(auto_mode_btn, paste_mode_btn)
    keyboard.row(back, close)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
    