import time

from src.database import api as database
from src.engine import swap as swap_engine
from src.engine.chain import token as token_engine

def start(user_id, lp_sniper_id):
  while True:
    lp_sniper = database.get_lp_sniper(user_id, lp_sniper_id)
    if lp_sniper:
      chain, token, amount, slippage, wallet_id = (
        lp_sniper['chain'],
        lp_sniper['token'],
        lp_sniper['amount'],
        lp_sniper['slippage'],
        lp_sniper['wallet_id']
      )
      if token_engine.check_liveness(chain, token):
        position = swap_engine.buy(user_id, chain, token, amount, slippage, wallet_id)
        swap_engine.sell(user_id, position['id'], 100, slippage)
        database.remove_lp_sniper(user_id, lp_sniper_id)
    else:
      break
    time.sleep(10)