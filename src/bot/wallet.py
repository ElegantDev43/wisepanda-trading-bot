from telebot import types

from src import database

def handle_wallet(bot, message):
    user = database.get_user(message.chat.id)

    text = f'''
*Settings > Wallets ({user.chain})*

Your currently added wallets:
1. [Balance](https://etherscan.io/address/0x3FfBa52e72D36ddf08012390b65C7Ef795ebf4B2) (0x3FfBa52e72D36ddf08012390b65C7Ef795ebf4B2): 0.000Ξ
2. [Balance](https://etherscan.io/address/0xF61fe8dfeb7F5c1520690F633e39daf538Aad308) (0xF61fe8dfeb7F5c1520690F633e39daf538Aad308): 0.000Ξ
    '''

    keyboard = types.InlineKeyboardMarkup()
    create_wallet = types.InlineKeyboardButton(text='Create Wallet', callback_data='create_wallet')
    import_wallet = types.InlineKeyboardButton(text='Import Wallet', callback_data='import_wallet')
    show_private_key = types.InlineKeyboardButton(text='Show Private Key', callback_data='show_private_key')
    keyboard.row(create_wallet)
    keyboard.row(import_wallet)
    keyboard.row(show_private_key)

    bot.send_message(message.chat.id, text, parse_mode='Markdown', disable_web_page_preview=True, reply_markup=keyboard)
