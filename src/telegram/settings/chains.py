from telebot import types

# import config
from src.database import api as user_model
from src.engine import api as main_api


def handle_chains(bot, message):
    # user = user_model.get_user_by_telegram(message.chat.id)
    chains = main_api.get_chains()
    current_chain = chains[main_api.get_chain(message.chat.id)]
    text = f'''
*Settings > Chains*

Current Chain: *🔗 {current_chain}*

Select the chain you'd like to use. You can only have one chain selected at the same time. Your defaults and presets will be different for each chain.
    '''

    buttons = []
    for chain in chains:
        caption = f'''✅ {chain}''' if chain == current_chain else chain
        button = types.InlineKeyboardButton(
            text=caption, callback_data=chain)
        buttons.append(button)
    back = types.InlineKeyboardButton('🔙 Back', callback_data='settings')

    keyboard = types.InlineKeyboardMarkup()
    for button in buttons:
        keyboard.row(button)
    keyboard.row(back)

    bot.send_message(chat_id=message.chat.id, text=text,
                     parse_mode='Markdown', reply_markup=keyboard)


def handle_select_chain(bot, message, next_chain):
    chains = main_api.get_chains()
    current_chain = chains[main_api.get_chain(message.chat.id)]
    if current_chain == next_chain:
        return
    if next_chain == "solana":
        next_chain_index = 0
    elif next_chain == "ethereum":
        next_chain_index = 1
    elif next_chain == "base":
        next_chain_index = 2
    user_model.set_chain(message.chat.id, next_chain_index)

    text = f'''
*Settings > Chains*

Current Chain: *🔗 {next_chain}*

Select the chain you'd like to use. You can only have one chain selected at the same time. Your defaults and presets will be different for each chain.
    '''
    buttons = []
    for chain in chains:
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
