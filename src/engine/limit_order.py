import time

from src.database import api as database

from src.engine.chain import token as token_engine
from src.engine.chain import dex as dex_engine

def start(user_id, limit_order_id):
  while True:
    limit_order = database.get_limit_order(user_id, limit_order_id)
    if limit_order:
      chain, type, token, amount, slippage, wallet, criteria = limit_order
      price = token_engine.get_market_data(chain, token)
      if type == 'buy':
        max_price = criteria
        valid = price < max_price
      else:
        min_price = criteria
        valid = price > min_price
      if valid:
        dex_engine.swap(chain, type, token, amount, slippage, wallet)
        database.remove_limit_order(user_id, limit_order_id)
    else:
      break
    time.sleep(10)