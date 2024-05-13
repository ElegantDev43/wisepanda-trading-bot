from telebot import types

import config
from src.database import user as user_model


def handle_keyboards(bot, message):
    # user = user_model.get_user_by_telegram(message.chat.id)
    buy_amounts = [0.1, 0.3, 0.5, 1]
    buy_count = len(buy_amounts)
    keyboard = types.InlineKeyboardMarkup()
    current_amount = 0.1
    text = '''
    *Settings > KeyBoards ⌨️*
    
    You can configure your trading keys here.
    '''
    buy_amount_buttons = []

    for amount in buy_amounts:
        caption = f' {amount}'
        button = types.InlineKeyboardButton(text=caption, callback_data=amount)
        buy_amount_buttons.append(button)

    back = types.InlineKeyboardButton('🔙 Back', callback_data='settings')

    gas_amounts = [10, 50, 100]
    gas_count = len(gas_amounts)

    gas_amount_buttons = []
    for amount in gas_amounts:
        caption = f' {amount}'
        button = types.InlineKeyboardButton(text=caption, callback_data=amount)
        gas_amount_buttons.append(button)

    sell_amounts = ['10%', '30%', '50%', '100%']
    sell_count = len(sell_amounts)

    sell_amount_buttons = []
    for amount in sell_amounts:
        caption = f' {amount}'
        button = types.InlineKeyboardButton(text=caption, callback_data=amount)
        sell_amount_buttons.append(button)

    set_buy_amount = types.InlineKeyboardButton(
        '----- 💰 Buy Amount -----', callback_data='buyer')

    set_gas_amount = types.InlineKeyboardButton(
        '----- ⛽️ Gas Amount -----', callback_data='buyer')

    set_sell_amount = types.InlineKeyboardButton(
        '----- 💰 Sell Amount -----', callback_data='buyer')

    keyboard.row(set_buy_amount)
    keyboard.row(*buy_amount_buttons[0:(buy_count // 2)])
    keyboard.row(*buy_amount_buttons[(buy_count // 2):buy_count])

    keyboard.row(set_gas_amount)
    keyboard.row(*gas_amount_buttons[(gas_count // 4):gas_count])

    keyboard.row(set_sell_amount)
    keyboard.row(*sell_amount_buttons[0:(sell_count // 2)])
    keyboard.row(*sell_amount_buttons[(sell_count // 2):sell_count])
    keyboard.row(back)

    bot.send_message(chat_id=message.chat.id, text=text,
                     parse_mode='Markdown', reply_markup=keyboard)


def handle_select_sell_amount(bot, message, next_amount):
    # user = user_model.get_user_by_telegram(message.chat.id)

    buy_amounts = [0.1, 0.3, 0.5, 1]
    buy_count = len(buy_amounts)
    keyboard = types.InlineKeyboardMarkup()
    text = '''
    *Settings > KeyBoards ⌨️*
    
    You can configure your trading keys here.
    '''
    buy_amount_buttons = []

    for amount in buy_amounts:
        caption = f' {amount}'
        button = types.InlineKeyboardButton(text=caption, callback_data=amount)
        buy_amount_buttons.append(button)

    sell_amount = ['10%', '30%', '50%', '100%']
    sell_count = len(sell_amount)

    sell_amount_buttons = []
    keyboard = types.InlineKeyboardMarkup()

    for amount in sell_amount:
        caption = f'🟢 {amount}' if amount == next_amount else amount
        button = types.InlineKeyboardButton(text=caption, callback_data=amount)
        sell_amount_buttons.append(button)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='settings')

    gas_amounts = [10, 50, 100]
    gas_count = len(gas_amounts)

    gas_amount_buttons = []
    for amount in gas_amounts:
        caption = f' {amount}'
        button = types.InlineKeyboardButton(text=caption, callback_data=amount)
        gas_amount_buttons.append(button)

    set_buy_amount = types.InlineKeyboardButton(
        '----- 💰 Buy Amount -----', callback_data='buyer')

    set_gas_amount = types.InlineKeyboardButton(
        '----- ⛽️ Gas Amount -----', callback_data='buyer')

    set_sell_amount = types.InlineKeyboardButton(
        '----- 💰 Sell Amount -----', callback_data='buyer')

    keyboard.row(set_buy_amount)
    keyboard.row(*buy_amount_buttons[0:(buy_count // 2)])
    keyboard.row(*buy_amount_buttons[(buy_count // 2):buy_count])

    keyboard.row(set_gas_amount)
    keyboard.row(*gas_amount_buttons[(gas_count // 4):gas_count])

    keyboard.row(set_sell_amount)
    keyboard.row(*sell_amount_buttons[0:(sell_count // 2)])
    keyboard.row(*sell_amount_buttons[(sell_count // 2):sell_count])
    keyboard.row(back)

    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id, text=text, parse_mode='Markdown')
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def handle_select_buy_amount(bot, message, next_amount):
    # user = user_model.get_user_by_telegram(message.chat.id)
    buy_amounts = ['0.1', '0.3', '0.5', '1']
    buy_count = len(buy_amounts)

    buy_amount_buttons = []
    keyboard = types.InlineKeyboardMarkup()

    text = '''
    *Settings > KeyBoards ⌨️*
    
    You can configure your trading keys here.
    '''

    for amount in buy_amounts:
        caption = f'🟢 {amount}' if amount == next_amount else amount
        button = types.InlineKeyboardButton(text=caption, callback_data=amount)
        buy_amount_buttons.append(button)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='settings')

    gas_amounts = [10, 50, 100]
    gas_count = len(gas_amounts)

    gas_amount_buttons = []
    for amount in gas_amounts:
        caption = f'⛽️ {amount}'
        button = types.InlineKeyboardButton(text=caption, callback_data=amount)
        gas_amount_buttons.append(button)

    sell_amounts = ['10%', '30%', '50%', '100%']
    sell_count = len(sell_amounts)

    sell_amount_buttons = []
    for amount in sell_amounts:
        caption = f'💰 {amount}'
        button = types.InlineKeyboardButton(text=caption, callback_data=amount)
        sell_amount_buttons.append(button)

    set_buy_amount = types.InlineKeyboardButton(
        '----- 💰 Buy Amount -----', callback_data='buyer')

    set_gas_amount = types.InlineKeyboardButton(
        '----- ⛽️ Gas Amount -----', callback_data='buyer')

    set_sell_amount = types.InlineKeyboardButton(
        '----- 💰 Sell Amount -----', callback_data='buyer')

    keyboard.row(set_buy_amount)
    keyboard.row(*buy_amount_buttons[0:(buy_count // 2)])
    keyboard.row(*buy_amount_buttons[(buy_count // 2):buy_count])

    keyboard.row(set_gas_amount)
    keyboard.row(*gas_amount_buttons[(gas_count // 4):gas_count])

    keyboard.row(set_sell_amount)
    keyboard.row(*sell_amount_buttons[0:(sell_count // 2)])
    keyboard.row(*sell_amount_buttons[(sell_count // 2):sell_count])
    keyboard.row(back)

    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id, text=text, parse_mode='Markdown')
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)


def handle_select_buy_amount(bot, message, next_amount):
    # user = user_model.get_user_by_telegram(message.chat.id)
    buy_amounts = ['0.1', '0.3', '0.5', '1']
    buy_count = len(buy_amounts)

    buy_amount_buttons = []
    keyboard = types.InlineKeyboardMarkup()

    text = '''
    *Settings > KeyBoards ⌨️*
    
    You can configure your trading keys here.
    '''

    for amount in buy_amounts:
        caption = f'🟢 {amount}' if amount == next_amount else amount
        button = types.InlineKeyboardButton(text=caption, callback_data=amount)
        buy_amount_buttons.append(button)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='settings')

    gas_amounts = [10, 50, 100]
    gas_count = len(gas_amounts)

    gas_amount_buttons = []
    for amount in gas_amounts:
        caption = f'⛽️ {amount}'
        button = types.InlineKeyboardButton(text=caption, callback_data=amount)
        gas_amount_buttons.append(button)

    sell_amounts = ['10%', '30%', '50%', '100%']
    sell_count = len(sell_amounts)

    sell_amount_buttons = []
    for amount in sell_amounts:
        caption = f'💰 {amount}'
        button = types.InlineKeyboardButton(text=caption, callback_data=amount)
        sell_amount_buttons.append(button)

    set_buy_amount = types.InlineKeyboardButton(
        '----- 💰 Buy Amount -----', callback_data='buyer')

    set_gas_amount = types.InlineKeyboardButton(
        '----- ⛽️ Gas Amount -----', callback_data='buyer')

    set_sell_amount = types.InlineKeyboardButton(
        '----- 💰 Sell Amount -----', callback_data='buyer')

    keyboard.row(set_buy_amount)
    keyboard.row(*buy_amount_buttons[0:(buy_count // 2)])
    keyboard.row(*buy_amount_buttons[(buy_count // 2):buy_count])

    keyboard.row(set_gas_amount)
    keyboard.row(*gas_amount_buttons[(gas_count // 4):gas_count])

    keyboard.row(set_sell_amount)
    keyboard.row(*sell_amount_buttons[0:(sell_count // 2)])
    keyboard.row(*sell_amount_buttons[(sell_count // 2):sell_count])
    keyboard.row(back)

    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id, text=text, parse_mode='Markdown')
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
