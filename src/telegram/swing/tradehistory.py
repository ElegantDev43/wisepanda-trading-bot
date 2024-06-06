from telebot import types

from src.database import swing as swing_model
from src.telegram.start import handle_start
# from src.database import user as user_model

def handle_tradehistory(bot, message):
    # user_model.create_user_by_telegram(message.chat.id)
    positions = swing_model.get_by_user_id(1)

    trading_tokens = ['A','B','C','D','E','F']
    trading_buttons = []

    print(positions)
    #token_count = len(trading_tokens)
    token_count = len(positions)

    for index in range(token_count):
        trading_buttons.append(types.InlineKeyboardButton(positions[index].token, callback_data=f'history_{positions[index].id}'))

    text = f'''
*📊️ Trade History*

Here you can see your swing trading history

💬 [Visit our Official Chat](https://t.me/wisepandaofficial)

🌍 [Visit our Website](https://www.wisepanda.ai)
    '''

    keyboard = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    for index in range(token_count):
        keyboard.row(trading_buttons[index])
    keyboard.row(back)

    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)


def handle_token_tradehistory(bot, message,swing_token):
    position = swing_model.get_by_swing_id(swing_token)

    winrate = 0
    if position.stop_count == 0 and position.sell_count == 0:
      winrate = 0
    else:
      winrate = position.sell_count/(position.sell_count + position.stop_count) * 100

    text = f'''
*📊️ Trade History*

Total Trades: {position.total_count}
Total Winning Trades: {position.sell_count}
Total Lost Trades: {position.stop_count}
Total Pips Won: 1902
Total P/L: $469
Total Pips Loss: 113
Average Returns: 344%
Winning Rates: {winrate}%

💬 [Visit our Official Chat](https://t.me/wisepandaofficial)

🌍 [Visit our Website](https://www.wisepanda.ai)
    '''

    keyboard = types.InlineKeyboardMarkup()
    stop = types.InlineKeyboardButton('🔴 Stop', callback_data=f'stop_{swing_token}')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='trade_history')
    keyboard.row(stop,back)

    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)


def handle_check_stop_trading(bot, message,swing_token):
    # user_model.create_user_by_telegram(message.chat.id)

    text = f'''
*📊️ Trade History*

*Really?*
⚠The position will be finished in : 3 days⚠

💬 [Visit our Official Chat](https://t.me/wisepandaofficial)

🌍 [Visit our Website](https://www.wisepanda.ai)
    '''

    keyboard = types.InlineKeyboardMarkup()
    stop = types.InlineKeyboardButton('☢️ Stop', callback_data=f'real_stop_{swing_token}')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='trade_history')
    keyboard.row(stop,back)

    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)


def handle_remove_swing_token(bot, message,swing_token):
    swing_model.remove_by_swing_id(swing_token)

    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    handle_start(bot, message)