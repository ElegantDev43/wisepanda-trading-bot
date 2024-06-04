from telebot import types

# import config
from src.database import user as user_model
from src.engine import api as main_api


def handle_keyboards(bot, message):
    # user = user_model.get_user_by_telegram(message.chat.id)
    keyboards = main_api.get_keyboards(message.chat.id)
    buy_amounts = keyboards['buy']
    gas_amounts = keyboards['gas']
    sell_amounts = keyboards['sell']

    text = '''
    *Settings > KeyBoards ⌨️*
    
    You can configure your trading keys here.
    '''

    keyboard = types.InlineKeyboardMarkup()

    buy_amount_buttons = []
    for index in range(len(buy_amounts)):
        caption = f'{buy_amounts[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f'select keyboard buy amount {index}')
        buy_amount_buttons.append(button)

    gas_amount_buttons = []
    for index in range(len(gas_amounts)):
        caption = f'{gas_amounts[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f'select keyboard gas amount {index}')
        gas_amount_buttons.append(button)

    sell_amount_buttons = []
    for index in range(len(sell_amounts)):
        caption = f'{sell_amounts[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f'select keyboard sell amount {index}')
        sell_amount_buttons.append(button)

    set_buy_amount = types.InlineKeyboardButton(
        '----- 💰 Buy Amount -----', callback_data='buyer')

    set_gas_amount = types.InlineKeyboardButton(
        '----- ⛽️ Gas Amount -----', callback_data='buyer')

    set_sell_amount = types.InlineKeyboardButton(
        '----- 💰 Sell Amount -----', callback_data='buyer')

    back = types.InlineKeyboardButton('🔙 Back', callback_data='settings')

    keyboard.row(set_buy_amount)
    keyboard.row(*buy_amount_buttons[0:(len(buy_amounts) // 2)])
    keyboard.row(
        *buy_amount_buttons[(len(buy_amounts) // 2): (len(buy_amounts))])

    keyboard.row(set_gas_amount)
    keyboard.row(*gas_amount_buttons[(len(gas_amounts) // 4):len(gas_amounts)])

    keyboard.row(set_sell_amount)
    keyboard.row(*sell_amount_buttons[0:(len(sell_amounts) // 2)])
    keyboard.row(
        *sell_amount_buttons[(len(sell_amounts) // 2):len(sell_amounts)])
    keyboard.row(back)

    bot.send_message(chat_id=message.chat.id, text=text,
                     parse_mode='Markdown', reply_markup=keyboard)


def handle_default_values(bot, message, item, index):
    bot.send_message(chat_id=message.chat.id, text='Enter Amount:')
    bot.register_next_step_handler_by_chat_id(
        chat_id=message.chat.id, callback=lambda next_message: handle_input_values(bot, next_message, item, index))


def handle_input_values(bot, message, item, index):
    value = message.text
    button_index = int(index)
    keyboards = main_api.get_keyboards(message.chat.id)
    buy_amounts = keyboards['buy']
    gas_amounts = keyboards['gas']
    sell_amounts = keyboards['sell']

    if item == 'buy':
        keyboards['buy'][button_index] = value
        main_api.update_keyboards(message.chat.id, keyboards)
    elif item == 'sell':
        keyboards['sell'][button_index] = f'{value}%'
        main_api.update_keyboards(message.chat.id, keyboards)
    elif item == 'gas':
        keyboards['gas'][button_index] = value
        main_api.update_keyboards(message.chat.id, keyboards)

    text = '''
    *Settings > KeyBoards ⌨️*
    
    You can configure your trading keys here.
    '''

    keyboard = types.InlineKeyboardMarkup()

    buy_amount_buttons = []
    for index in range(len(buy_amounts)):
        caption = f'{buy_amounts[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f'select keyboard buy amount {index}')
        buy_amount_buttons.append(button)

    gas_amount_buttons = []
    for index in range(len(gas_amounts)):
        caption = f'{gas_amounts[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f'select keyboard gas amount {index}')
        gas_amount_buttons.append(button)

    sell_amount_buttons = []
    for index in range(len(sell_amounts)):
        caption = f'{sell_amounts[index]}'
        button = types.InlineKeyboardButton(
            text=caption, callback_data=f'select keyboard sell amount {index}')
        sell_amount_buttons.append(button)

    set_buy_amount = types.InlineKeyboardButton(
        '----- 💰 Buy Amount -----', callback_data='buyer')

    set_gas_amount = types.InlineKeyboardButton(
        '----- ⛽️ Gas Amount -----', callback_data='buyer')

    set_sell_amount = types.InlineKeyboardButton(
        '----- 💰 Sell Amount -----', callback_data='buyer')

    back = types.InlineKeyboardButton('🔙 Back', callback_data='settings')

    keyboard.row(set_buy_amount)
    keyboard.row(*buy_amount_buttons[0:(len(buy_amounts) // 2)])
    keyboard.row(
        *buy_amount_buttons[(len(buy_amounts) // 2): (len(buy_amounts))])

    keyboard.row(set_gas_amount)
    keyboard.row(*gas_amount_buttons[(len(gas_amounts) // 4):len(gas_amounts)])

    keyboard.row(set_sell_amount)
    keyboard.row(*sell_amount_buttons[0:(len(sell_amounts) // 2)])
    keyboard.row(
        *sell_amount_buttons[(len(sell_amounts) // 2):len(sell_amounts)])
    keyboard.row(back)

    bot.send_message(chat_id=message.chat.id, text=text,
                     parse_mode='Markdown', reply_markup=keyboard)
