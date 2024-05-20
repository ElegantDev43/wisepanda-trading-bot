from telebot import types

# import config
from src.database import user as user_model
# from src.engine import main as engine

explorers = {
    'ethereum': 'https://etherscan.io/address/',
    'solana': 'https://solscan.io/account/',
}


def handle_wallets(bot, message):
    user = user_model.get_user_by_telegram(message.chat.id)
    chain = user.chain
    wallets = user.wallets[chain]

    text = f'''
*Settings > Wallets (🔗 {chain})*

You can use up to 4 multiple wallets.

Your currently added wallets:
'''
    for index, wallet in enumerate(wallets, start=1):
        text += f'''
{index}. Balance: {wallet['balance']:.3f}Ξ
[{wallet['address']}]({explorers[chain] + wallet['address']})
'''

    keyboard = types.InlineKeyboardMarkup()
    create_wallet = types.InlineKeyboardButton(
        text='Create Wallet', callback_data='create_wallet')
    import_wallet = types.InlineKeyboardButton(
        text='Import Wallet', callback_data='import_wallet')
    remove_wallet = types.InlineKeyboardButton(
        text='Remove Wallet', callback_data='remove_wallet')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='settings')
    keyboard.row(create_wallet)
    keyboard.row(import_wallet)
    keyboard.row(remove_wallet)
    keyboard.row(back)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def handle_create_wallet(bot, message):
    user = user_model.get_user_by_telegram(message.chat.id)
    chain = user.chain

    if len(user.wallets[chain]) == config.WALLET_COUNT:
        bot.send_message(chat_id=message.chat.id,
                         text='Exceed wallets limit of 3')
        return

    address, private_key = engine.create_wallet(chain)
    user.wallets[chain].append(
        {'address': address, 'private_key': private_key, 'balance': 0, 'active': False})
    user_model.update_user_by_id(user.id, 'wallets', user.wallets)

    text = f'''
✅ A new wallet has been generated for you. Save the private key below❗:

Address: {address}
Private Key: {private_key}
    '''

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')

    handle_wallets(bot, message)


def handle_import_wallet(bot, message):
    user = user_model.get_user_by_telegram(message.chat.id)
    chain = user.chain

    if len(user.wallets[chain]) == config.WALLET_COUNT:
        bot.send_message(chat_id=message.chat.id,
                         text='Exceed wallets limit of 3')
        return

    bot.send_message(chat_id=message.chat.id, text='Enter private key:')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_private_key(bot, next_message))


def handle_remove_wallet(bot, message):
    user = user_model.get_user_by_telegram(message.chat.id)
    chain = user.chain
    wallets = ['1', '2', '3', '4', '5']
    wallet_count = len(wallets)

    text = f'''
*Settings > Wallets (🔗 {chain})*

You can remove wallets here.

Your currently added {wallet_count} wallets:
'''

    keyboard = types.InlineKeyboardMarkup()
  #  for index in range(wallet_count):
   #     wallets.append(types.InlineKeyboardButton(
  #          f'W{index + 1}{" 🟢" if user_wallets[index]['active'] == True else ""}', callback_data=f'manual wallet {index}'))
    back = types.InlineKeyboardButton('🔙 Back', callback_data='wallets')

    for index in range(wallet_count):
        keyboard.row(wallets[index])
    keyboard.row(back)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def handle_input_private_key(bot, message):
    user = user_model.get_user_by_telegram(message.chat.id)
    chain = user.chain
    private_key = message.text
    address = engine.import_wallet(chain, private_key)
    balance = engine.get_balance(chain, address)
    user.wallets[chain].append(
        {'address': address, 'private_key': private_key, 'balance': balance, 'active': False})
    user_model.update_user_by_id(user.id, 'wallets', user.wallets)

    text = f'''
✅ A new wallet has been imported for you. Save the private key below❗:

Address: {address}
Private Key: {private_key}
    '''

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')

    handle_wallets(bot, message)
