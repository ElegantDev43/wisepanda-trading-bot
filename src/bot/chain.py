from telebot import types

from src import config, database

def handle_chain(bot, message):
    user = database.get_user(message.chat.id)
    currentChain = user.chain

    text = f'''
*Settings > Chains*

Current Chain: {currentChain}

Select the chain you'd like to use. You can only have one chain selected at the same time. Your defaults and presets will be different for each chain.
    '''

    buttons = []
    for chain in config.CHAINS:
        caption = f'* {chain}' if chain == currentChain else chain
        button = types.InlineKeyboardButton(text=caption, callback_data=chain)
        buttons.append(button)

    keyboard = types.InlineKeyboardMarkup()
    for button in buttons:
        keyboard.row(button)

    bot.send_message(message.chat.id, text, parse_mode='Markdown', disable_web_page_preview=True, reply_markup=keyboard)

def handle_select_chain(bot, message, paramChain):
    user = database.get_user(message.chat.id)
    if user.chain == paramChain:
        return
    database.update_user(message.chat.id, 'chain', paramChain)

    text = f'''
*Settings > Chains*

Current Chain: {paramChain}

Select the chain you'd like to use. You can only have one chain selected at the same time. Your defaults and presets will be different for each chain.
    '''

    buttons = []
    for chain in config.CHAINS:
        caption = f'* {chain}' if chain == paramChain else chain
        button = types.InlineKeyboardButton(text=caption, callback_data=chain)
        buttons.append(button)

    keyboard = types.InlineKeyboardMarkup()
    for button in buttons:
        keyboard.row(button)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, parse_mode='Markdown')
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
