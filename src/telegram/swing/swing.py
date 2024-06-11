from telebot import types

# from src.database import user as user_model

def handle_start(bot, message):
    # user_model.create_user_by_telegram(message.chat.id)

    hot_bearish_tokens = ['A','B','C','D','E','F']
    hot_bullish_tokens = ['G','H','I','J','K','L']
    bearish_buttons = []
    bullish_buttons = []

    token_count = len(hot_bearish_tokens)


    for index in range(token_count):
        bearish_buttons.append(types.InlineKeyboardButton(hot_bearish_tokens[index], callback_data=f'auto - bearish token {index}'))
        bullish_buttons.append(types.InlineKeyboardButton(hot_bullish_tokens[index], callback_data=f'auto - bullish token {index}'))

    text = '''
*Welcome to Swing Trading!*
Discover and engage with the newest tokens as they launch. Gain a competitive edge with early investment opportunities.

💬 [Visit our Official Chat](https://t.me/wisepandaofficial)

🌍 [Visit our Website](https://www.wisepanda.ai)
    '''

    keyboard = types.InlineKeyboardMarkup()
    short_bearish_tokens = types.InlineKeyboardButton('📉 Short Bearish Tokens', callback_data='Default')
    medium_bearish_tokens = types.InlineKeyboardButton('📉 Medium Bearish Tokens', callback_data='Default')
    long_bearish_tokens = types.InlineKeyboardButton('📉 Long Bearish Tokens', callback_data='Default')
    short_bullish_tokens = types.InlineKeyboardButton('📈 Short Bullish Tokens', callback_data='Default')
    medium_bullish_tokens = types.InlineKeyboardButton('📈 Medium Bullish Tokens', callback_data='Default')
    long_bullish_tokens = types.InlineKeyboardButton('📈 Long Bullish Tokens', callback_data='Default')
    select_token = types.InlineKeyboardButton('🤏 Select Token', callback_data='select_token')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    trade_history = types.InlineKeyboardButton('📊 Trade History', callback_data='trade_history')
    keyboard.row(short_bearish_tokens, short_bullish_tokens)
    keyboard.row(bearish_buttons[0],bearish_buttons[1],bullish_buttons[0],bullish_buttons[1])
    keyboard.row(medium_bearish_tokens, medium_bullish_tokens)
    keyboard.row(bearish_buttons[2],bearish_buttons[3],bullish_buttons[2],bullish_buttons[3])
    keyboard.row(long_bearish_tokens, long_bullish_tokens)
    keyboard.row(bearish_buttons[4],bearish_buttons[5],bullish_buttons[4],bullish_buttons[5])
    keyboard.row(select_token)
    keyboard.row(trade_history,back)

    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)