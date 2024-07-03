import time

from src.database import api as database
from src.engine import swap as swap_engine
from src.engine.chain import token as token_engine

def start(user_id, position_id):
  print('Successfully started stop_loss engine')
  while True:
    position = database.get_position(user_id, position_id)
    print(position)
    if position:
      market_cap = position['market_capital']
      token = position['token']
      chain = position['chain']
      stop_loss = position['stop_loss']
      current_market_data = token_engine.get_market_data(chain, token)
      print(current_market_data['market_capital'] / market_cap * 100)
      if market_cap > current_market_data['market_capital']:
        
        if (1 - (current_market_data['market_capital'] / market_cap)) * 100 >= stop_loss:
          swap_engine.sell(user_id, position_id, 100, 90)
          print(f"stop_loss sell: {position_id}")
          token_snipers = database.get_token_snipers(user_id, chain)
          for index in range(len(token_snipers)):
            if token_snipers[index]['is_auto'] == True:
              database.remove_token_sniper(user_id, token_snipers[index]['id'])
              break
    else:
      break
    time.sleep(3)