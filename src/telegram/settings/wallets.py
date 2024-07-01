from telebot import types

# import config
from src.database import user as user_model
# from src.engine import main as engine
from src.engine.chain import wallet as wallet_manage
from src.engine import api as main_api

explorers = {
    'ethereum': 'https://etherscan.io/address/',
    'solana': 'https://solscan.io/account/',
}


def handle_wallets(bot, message):
   # user = user_model.get_user_by_telegram(message.chat.id)
    current_chain_index = main_api.get_chain(message.chat.id)
    wallets = main_api.get_wallets(message.chat.id)

    chains = main_api.get_chains()
    current_chain = chains[current_chain_index]
    
    for index in range(len(wallets)):
      wallets[index]['balance'] = main_api.get_wallet_balance(message.chat.id, wallets[index]['id'])

    wallet_count = len(wallets)
    text = f'''
*Settings > Wallets (🔗 {current_chain})*

You can use up to 100 multiple wallets.

Your currently added {wallet_count} wallets:
'''
    for wallet in wallets:
        text += f'''* Address :* {wallet['address']
                                  }, *Balance : *{float(wallet['balance'] / 10 ** 9)}SOL\n'''
    keyboard = types.InlineKeyboardMarkup()
    create_wallet = types.InlineKeyboardButton(
        text='Create Wallet', callback_data='create_wallet')
    import_wallet = types.InlineKeyboardButton(
        text='Import Wallet', callback_data='import_wallet')
    remove_wallet = types.InlineKeyboardButton(
        text='Remove Wallet', callback_data='remove_wallet')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='settings')
    keyboard.row(create_wallet, import_wallet)
    keyboard.row(remove_wallet)
    keyboard.row(back)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard, disable_web_page_preview=True)


def handle_create_wallet(bot, message):
    # user = user_model.get_user_by_telegram(message.chat.id)
    chains = main_api.get_chains()
    current_chain_index = main_api.get_chain(message.chat.id)

    wallets = main_api.get_wallets(message.chat.id)
    if len(wallets) == 100:
        bot.send_message(chat_id=message.chat.id,
                         text='Exceed wallets limit of 100')
        return
    else:
        new_wallet = main_api.create_wallet(message.chat.id, 'AAA')
        text = f'''
✅ A new wallet has been generated for you. Save the private key below❗:

Address: {new_wallet['address']}
Private Key: {new_wallet['private_key']}
    '''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')

    handle_wallets(bot, message)


def handle_import_wallet(bot, message):
   # user = user_model.get_user_by_telegram(message.chat.id)
    # chain = user.chain
    chains = main_api.get_chains()
    current_chain_index = main_api.get_chain(message.chat.id)
    wallets = main_api.get_wallets(message.chat.id)
    if len(wallets) == 100:
        bot.send_message(chat_id=message.chat.id,
                         text='Exceed wallets limit of 5')
        return

    bot.send_message(chat_id=message.chat.id, text='Enter private key:')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_private_key(bot, next_message))


def handle_remove_wallet(bot, message):
    # user = user_model.get_user_by_telegram(message.chat.id)
    chains = main_api.get_chains()
    current_chain_index = main_api.get_chain(message.chat.id)
    wallets = main_api.get_wallets(message.chat.id)
    text = f'''
*Settings > Wallets (🔗 {chains[current_chain_index]})*

You can remove wallets here.
Select a wallet to remove.
Your currently added {len(wallets)} wallets:
'''

    for index in range(len(wallets)):
      wallets[index]['balance'] = main_api.get_wallet_balance(message.chat.id, wallets[index]['id'])

    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    for index in range(len(wallets)):
        caption = f'''⭕ Address : {wallets[index]['address']
                                   },  Balance : {wallets[index]['balance']}'''
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f'''select_remove_wallet {wallets[index]['id']}''')
        buttons.append(button)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='wallets')

    for button in buttons:
        keyboard.row(button)
    keyboard.row(back)
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown',
                     reply_markup=keyboard)


def remove_selected_wallet(bot, message, index):
    wallet_index = float(index)
    wallets = main_api.get_wallets(message.chat.id)
    main_api.remove_wallet(message.chat.id, wallet_index)
    text = f'''
✅ Successfully removed a wallet❗:
    '''
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')
    handle_remove_wallet(bot, message)


def handle_input_private_key(bot, message):
    # user = user_model.get_user_by_telegram(message.chat.id)
    private_key = message.text
    wallet = main_api.import_wallet(message.chat.id, private_key, 'AAA')
    balance = main_api.get_wallet_balance(message.chat.id, wallet['id'])
    text = f'''
✅ A new wallet has been imported for you. Save the private key below❗:

Address: {wallet['address']}
Balance: {float(balance / (10 ** 9))} SOL
    '''

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')

    handle_wallets(bot, message)
