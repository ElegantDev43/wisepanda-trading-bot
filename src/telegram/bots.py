from telebot import types

import config


def handle_bots(bot, message):
    text = '''
*Backup Bots*

Whenever we experience higher loads, you can use these backup bots. All your settings and personal information will remain the same across them.
    '''

    keyboard = types.InlineKeyboardMarkup()
    for index in range(config.BOT_COUNT):
        url = f'https://t.me/{config.BOT_USERNAME}{"" if index ==
                                                   0 else index}'
        keyboard.row(types.InlineKeyboardButton(
            f'{config.BOT_NAME[index]}', url=url))
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    close = types.InlineKeyboardButton('❌ Close', callback_data='close')
    keyboard.row(back, close)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)
