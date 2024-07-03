import time

from src.database import api as database
from src.engine import swap as swap_engine
from src.engine.chain import token as token_engine

def start(user_id, token_sniper_id):
  while True:
    token_sniper = database.get_token_sniper(user_id, token_sniper_id)
    if token_sniper:
      stage, chain, token, amount, slippage, wallet_id, auto_sell, stop_loss = (
        token_sniper['stage'],
        token_sniper['chain'],
        token_sniper['token'],
        token_sniper['amount'],
        token_sniper['slippage'],
        token_sniper['wallet_id'],
        token_sniper['auto_sell'],
        token_sniper['stop_loss']
      )
      if stage == 'buy':
        if token_engine.check_liveness(chain, token):
          position = swap_engine.buy(user_id, chain, token, amount, slippage, wallet_id, stop_loss)
          print('Token Sniper Buy', position['id'])
          if len(auto_sell) == 0:
            database.remove_token_sniper(user_id, token_sniper_id)
            print('sniper sell done')
          else:
            token_sniper['stage'] = 'sell'
            token_sniper['position_id'] = position['id']
            database.set_token_sniper(user_id, token_sniper_id, token_sniper)
      else:
        sell = auto_sell[0]
        auto_sell.pop(0)
        position = database.get_position(user_id, token_sniper['position_id'])
        market_capital = token_engine.get_market_data(chain, token)['market_capital']
        if market_capital >= position['market_capital'] * (1 + sell['profit']):
          print(slippage)
          swap_engine.sell(user_id, position['id'], sell['amount'], slippage)
          print('Token Sniper Sell', position['id'])
          if len(auto_sell) == 0:
            database.remove_token_sniper(user_id, token_sniper_id)
            print('sniper sell done')
            return
          else:
            token_sniper['auto_sell'] = auto_sell
            database.set_token_sniper(user_id, token_sniper_id, token_sniper)
    else:
      break
    time.sleep(3)