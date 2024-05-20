from telebot import types


def handle_settings(bot, message):
    text = f'''
*Settings*

Select an option below to configure:
    '''

    keyboard = types.InlineKeyboardMarkup()
    chains = types.InlineKeyboardButton('⛓️ Chains', callback_data='chains')
    wallets = types.InlineKeyboardButton('💳 Wallets', callback_data='wallets')
    criterias = types.InlineKeyboardButton(
        '🔍 Criteria', callback_data='criterias')
    keyboards = types.InlineKeyboardButton(
        '⌨️ Keyboard', callback_data='keyboards')
    auto_orders = types.InlineKeyboardButton(
        '🎮 Auto order', callback_data='auto-orders')
    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    keyboard.row(chains)
    keyboard.row(wallets)
    keyboard.row(criterias)
    keyboard.row(keyboards)
    keyboard.row(auto_orders)
    keyboard.row(back)

    bot.send_message(chat_id=message.chat.id, text=text,
                     parse_mode='Markdown', reply_markup=keyboard)
