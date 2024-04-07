from telebot import types

import config
from src.database import user as user_model

def handle_chains(bot, message):
    user = user_model.get_user(message.chat.id)
    current_chain = user.chain

    text = f'''
*Settings > Chains*

Current Chain: *🔗{current_chain}*

Select the chain you'd like to use. You can only have one chain selected at the same time. Your defaults and presets will be different for each chain.
    '''

    buttons = []
    for chain in config.CHAINS:
        caption = f'✅ {chain}' if chain == current_chain else chain
        button = types.InlineKeyboardButton(text=caption, callback_data=chain)
        buttons.append(button)

    keyboard = types.InlineKeyboardMarkup()
    for button in buttons:
        keyboard.row(button)

    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard)

def handle_select_chain(bot, message, next_chain):
    user = user_model.get_user(message.chat.id)
    if user.chain == next_chain:
        return
    user_model.update_user(user.id, 'chain', next_chain)

    text = f'''
*Settings > Chains*

Current Chain: *🔗{next_chain}*

Select the chain you'd like to use. You can only have one chain selected at the same time. Your defaults and presets will be different for each chain.
    '''

    buttons = []
    for chain in config.CHAINS:
        caption = f'✅ {chain}' if chain == next_chain else chain
        button = types.InlineKeyboardButton(text=caption, callback_data=chain)
        buttons.append(button)

    keyboard = types.InlineKeyboardMarkup()
    for button in buttons:
        keyboard.row(button)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, parse_mode='Markdown')
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
