import time

from src.database import api as database
from src.engine import swap as swap_engine
from src.engine.chain import token as token_engine

def start(user_id, limit_order_id):
  while True:
    limit_order = database.get_limit_order(user_id, limit_order_id)
    if limit_order:
      if limit_order['type'] == 'buy':
        chain, token, amount, slippage, wallet_id, max_market_capital, stop_loss = (
          limit_order['chain'],
          limit_order['token'],
          limit_order['amount'],
          limit_order['slippage'],
          limit_order['wallet_id'],
          limit_order['max_market_capital'],
          limit_order['stop-loss']
        )
        market_capital = token_engine.get_market_data(chain, token)['market_capital']
        if market_capital <= max_market_capital:
          position = swap_engine.buy(user_id, chain, token, amount, slippage, wallet_id, stop_loss)
          print('Limit Buy', position['id'])
          database.remove_limit_order(user_id, limit_order_id)
      else:
        position_id, amount, slippage, profit = (
          limit_order['position_id'],
          limit_order['amount'],
          limit_order['slippage'],
          limit_order['profit']
        )
        position = database.get_position(user_id, position_id)
        market_capital = token_engine.get_market_data(chain, token)['market_capital']
        if market_capital >= position['market_capital'] * (1 + profit):
          swap_engine.sell(user_id, position_id, amount, slippage)
          print('Limit Sell', position['id'])
          database.remove_limit_order(user_id, limit_order_id)
    else:
      break
    time.sleep(10)