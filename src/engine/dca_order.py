import time

from src.database import api as database
from src.engine import swap as swap_engine
from src.engine.chain import token as token_engine

def start(user_id, dca_order_id):
  while True:
    dca_order = database.get_dca_order(user_id, dca_order_id)
    if dca_order:
      if 'criteria':
        if dca_order['type'] == 'buy':
          id, type, chain, token, amount, slippage, wallet_id, criteria, interval, count, stop_loss = dca_order
          swap_engine.buy(user_id, chain, token, amount, slippage, wallet_id, stop_loss)
        else:
          id, type, position_id, amount, slippage, criteria, interval, count = dca_order
          swap_engine.sell(user_id, position_id, amount, slippage)
        count -= 1
        if count != 0:
          dca_order['count'] = count
          database.set_dca_order(user_id, dca_order_id, dca_order)
        else:
          database.remove_dca_order(user_id, dca_order_id)
    else:
      break
    time.sleep(interval)