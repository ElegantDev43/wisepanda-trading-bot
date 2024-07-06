import time

from src.database import api as database
from src.engine import swap as swap_engine

def start(user_id, dca_order_id):
  while True:
    dca_order = database.get_dca_order(user_id, dca_order_id)
    if dca_order:
      if dca_order['type'] == 'buy':
        chain, token, amount, slippage, wallet_id, interval, count, stop_loss = (
          dca_order['chain'],
          dca_order['token'],
          dca_order['amount'],
          dca_order['slippage'],
          dca_order['wallet_id'],
          dca_order['interval'],
          dca_order['count'],
          dca_order['stop_loss']
        )
        position = swap_engine.buy(user_id, chain, token, amount, slippage, wallet_id, stop_loss)
        print('DCA Buy', position['id'])
        count -= 1
        if count != 0:
          dca_order['count'] = count
          database.set_dca_order(user_id, dca_order_id, dca_order)
        else:
          database.remove_dca_order(user_id, dca_order_id)
      else:
        position_id, amount, slippage, interval, count = (
          dca_order['position_id'],
          dca_order['amount'],
          dca_order['slippage'],
          dca_order['interval'],
          dca_order['count']
        )
        position = database.get_position(user_id, position_id)
        swap_engine.sell(user_id, position_id, amount, slippage)
        print('DCA Sell', position['id'])
        count -= 1
        if count != 0:
          dca_order['count'] = count
          database.set_dca_order(user_id, dca_order_id, dca_order)
        else:
          database.remove_dca_order(user_id, dca_order_id)
    else:
      break
    time.sleep(interval)