from telebot import types

import config
from src import database
from src.ethereum import wallet as ethereum_wallet
from src.solana import wallet as solana_wallet

def handle_wallet(bot, message):
    user = database.get_user(message.chat.id)
    chain = user.chain
    wallets = user.wallets[chain]

    text = f'''
*Settings > Wallet (🔗{user.chain})*

Your currently added wallets:
'''
    for index, wallet in enumerate(wallets, start=1):
        text += f"{index}. [Balance](https://etherscan.io/address/{wallet['address']}) ({wallet['address']}): 0.000Ξ\n"

    keyboard = types.InlineKeyboardMarkup()
    create_wallet = types.InlineKeyboardButton(text='Create Wallet', callback_data='create_wallet')
    import_wallet = types.InlineKeyboardButton(text='Import Wallet', callback_data='import_wallet')
    keyboard.row(create_wallet)
    keyboard.row(import_wallet)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)

def handle_create_wallet(bot, message):
    user = database.get_user(message.chat.id)
    chain = user.chain

    if len(user.wallets[chain]) == config.WALLET_COUNT:
        bot.send_message(chat_id=message.chat.id, text='Exceed wallet count limit of 3')
        return

    if chain == 'ethereum':
        wallet = ethereum_wallet
    elif chain == 'solana':
        wallet = solana_wallet

    address, private_key = wallet.create_wallet()

    user.wallets[chain].append({'address': address, 'private_key': private_key})
    database.update_user(user.id, 'wallets', user.wallets)

    text = f'''
✅ A new wallet has been generated for you. Save the private key below❗:

Address: {address}
Private Key: {private_key}
    '''

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')

def handle_import_wallet(bot, message):
    user = database.get_user(message.chat.id)
    chain = user.chain

    if len(user.wallets[chain]) == config.WALLET_COUNT:
        bot.send_message(chat_id=message.chat.id, text='Exceed wallet count limit of 3')
        return

    bot.send_message(chat_id=message.chat.id, text='Enter private key:')
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=lambda msg: handle_input_private_key(bot, msg))

def handle_input_private_key(bot, message):
    user = database.get_user(message.chat.id)
    chain = user.chain

    if chain == 'ethereum':
        wallet = ethereum_wallet
    elif chain == 'solana':
        wallet = solana_wallet

    private_key = message.text
    print(f'message.text: {message.text}')
    address = wallet.get_address(private_key)

    user.wallets[chain].append({'address': address, 'private_key': private_key})
    database.update_user(user.id, 'wallets', user.wallets)

    text = f'''
✅ A new wallet has been imported for you. Save the private key below❗:

Address: {address}
Private Key: {private_key}
    '''

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')