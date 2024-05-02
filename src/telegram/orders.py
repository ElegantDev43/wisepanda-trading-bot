from telebot import types

import config
from src.database import user as user_model

def handle_orders(bot, message):
    user = user_model.get_user_by_telegram(message.chat.id)

    text = f'''
*Pending Orders*

You currently have {len(user.orders)} pending orders.

Your orders are:
    '''

    for order in user.orders:
            text += f'''
Chain: {order['chain']}
Token: {order['token']}
Order: {order['type']}
Amount: {order['amount']}
Transaction: [{order['transaction']}](https://sepolia.etherscan.io/tx/{order['transaction']})
            '''

    keyboard = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(back)
    keyboard.row(close)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)