import time

from src.database import api as database
from src.engine import swap as swap_engine

def start(user_id, limit_order_id):
  while True:
    limit_order = database.get_limit_order(user_id, limit_order_id)
    if limit_order:
      if 'criteria':
        if limit_order['type'] == 'buy':
          id, type, chain, token, amount, slippage, wallet_id, stop_loss, criteria = limit_order
          swap_engine.buy(user_id, chain, token, amount, slippage, wallet_id, stop_loss)
        else:
          id, type, position_id, amount, slippage, criteria = limit_order
          swap_engine.sell(user_id, position_id, amount, slippage)
        database.remove_limit_order(user_id, limit_order_id)
    else:
      break
    time.sleep(10)