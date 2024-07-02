import time

from src.database import api as database
from src.engine import swap as swap_engine
from src.engine.chain import token as token_engine

def start(user_id, position_id):
  while True:
    position = database.get_position(user_id, position_id)
    if position:
      market_cap = position['market_capital']
      token = position['token']
      chain = position['chain']
      stop_loss = position['stop_loss']
      current_market_cap = token_engine.get_market_data(chain, token)
      if market_cap > current_market_cap['market_capital']:
        print(current_market_cap['market_capital'] / market_cap * 100)
        if (1 - (current_market_cap['market_capital'] / market_cap)) * 100 >= stop_loss:
          swap_engine.sell(user_id, position_id, 100, 10)
          print(f"stop_loss sell: {position_id}")
    else:
      break
    time.sleep(3)