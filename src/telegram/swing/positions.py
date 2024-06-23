import time
from telebot import types

from src.engine import api as main_api
from src.telegram.start import handle_start

sample_positions = [
  {
    'id': 1,
    'chain': 0,
    'token': '5oVNBeEEQvYi1cX3ir8Dx5n1P7pdxydbGF2X4TxVusJm',
    'amount': {
      'in': 1000,
      'out': 1200
    },
    'wallet_id': 1719102231.3135822,
    'stop_loss': 50
  },
  {
    'id': 2,
    'chain': 0,
    'token': '5oVNBeEEQvYi1cX3ir8Dx5n1P7pdxydbGF2X4TxVusJm',
    'amount': {
      'in': 1300,
      'out': 1100
    },
    'wallet_id': 1719102231.3135822,
    'stop_loss': 50
  }
]

def handle_open_positions(bot, message):
    # user_model.create_user_by_telegram(message.chat.id)
    chain_positions = main_api.get_positions(message.chat.id)

    text = f'''
*📊️ Open Positions*

You currently have {len(chain_positions)} positions.

Select position to sell tokens.

💬 [Visit our Official Chat](https://t.me/wisepandaofficial)

🌍 [Visit our Website](https://www.wisepanda.ai)
    '''

    keyboard = types.InlineKeyboardMarkup()
    
    position_btns = []

    for position in sample_positions:
      position_btns.append(types.InlineKeyboardButton(position['token'], callback_data=f'swing_position_{position['id']}'))  

    # for position in chain_positions:
    #   position_btns.append(types.InlineKeyboardButton(position['token'], callback_data=f'swing_position_{position['id']}'))  

    back = types.InlineKeyboardButton('🔙 Back', callback_data='start')
    
    for position_btn in position_btns:
      keyboard.row(position_btn)
    
    keyboard.row(back)

    # bot.delete_message(chat_id = message.chat.id, message_id = message.message_id, timeout = 0 )
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)
