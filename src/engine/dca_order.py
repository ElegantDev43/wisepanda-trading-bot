import time

from src.database import api as database

from src.engine.chain import token as token_engine
from src.engine.chain import dex as dex_engine

def start(user_id, dca_order_id):
  while True:
    dca_order = database.get_dca_order(user_id, dca_order_id)
    if dca_order:
      chain, type, token, amount, slippage, wallet_id, criteria, interval, count = dca_order
      price = token_engine.get_market_data(chain, token)
      if type == 'buy':
        max_price = criteria
        valid = price < max_price
      else:
        min_price = criteria
        valid = price > min_price
      if valid:
        wallet = database.get_wallet(user_id, chain, wallet_id)
        dex_engine.swap(chain, type, token, amount, slippage, wallet)
        count -= 1
        if count != 0:
          dca_order['count'] = count
          database.set_dca_order(user_id, dca_order_id, dca_order)
        else:
          database.remove_dca_order(user_id, dca_order_id)
    else:
      break
    time.sleep(interval)