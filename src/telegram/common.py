from telebot import types

from src.database import user as user_model
from src.engine import main as engine
from src.telegram import auto_sniper, manual_buyer

def handle_auto_sniper_or_manual_buyer(bot, message):
    user_model.create_user(message.chat.id)

    text = '''
*Auto Sniper / Manual Buyer*
Paste in a token address below to start buying
e.g. 0x6982508145454Ce325dDbE47a25d4ec3d2311933
    '''

    bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=lambda next_message: handle_input_token(bot, next_message))

def handle_input_token(bot, message):
    user = user_model.get_user(message.chat.id)
    user_chain = user.chain

    token = message.text
    token_chain = engine.get_token_chain(token)

    if token_chain == None:
        bot.send_message(chat_id=message.chat.id, text='Invalid token address')
        return

    if user_chain != token_chain:
        user_model.update_user(user.id, 'chain', token_chain)

    if engine.get_token_information(token) == None:
        auto_sniper.handle_auto_sniper(bot, message)
    else:
        manual_buyer.handle_manual_buyer(bot, message)
