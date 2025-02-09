from telebot import types

# import config
from src.database import user as user_model


def handle_chains(bot, message):
    # user = user_model.get_user_by_telegram(message.chat.id)
    chains = ['ethereum', 'solana', 'base']
    current_chain = 'ethereum'

    text = f'''
*Settings > Chains*

Current Chain: *🔗 {current_chain}*

Select the chain you'd like to use. You can only have one chain selected at the same time. Your defaults and presets will be different for each chain.
    '''

    buttons = []
    for chain in chains:
        caption = f'✅ {chain}' if chain == current_chain else chain
        button = types.InlineKeyboardButton(text=caption, callback_data=chain)
        buttons.append(button)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='settings')

    keyboard = types.InlineKeyboardMarkup()
    for button in buttons:
        keyboard.row(button)
    keyboard.row(back)

    bot.send_message(chat_id=message.chat.id, text=text,
                     parse_mode='Markdown', reply_markup=keyboard)


def handle_select_chain(bot, message, next_chain):
    user = user_model.get_user_by_telegram(message.chat.id)
    if user.chain == next_chain:
        return
    user_model.update_user_by_id(user.id, 'chain', next_chain)

    text = f'''
*Settings > Chains*

Current Chain: *🔗 {next_chain}*

Select the chain you'd like to use. You can only have one chain selected at the same time. Your defaults and presets will be different for each chain.
    '''
    buttons = []
    for chain in user.chain:
        caption = f'✅ {chain}' if chain == next_chain else chain
        button = types.InlineKeyboardButton(text=caption, callback_data=chain)
        buttons.append(button)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='settings')

    keyboard = types.InlineKeyboardMarkup()
    for button in buttons:
        keyboard.row(button)
    keyboard.row(back)

    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id, text=text, parse_mode='Markdown')
    bot.edit_message_reply_markup(
        chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
