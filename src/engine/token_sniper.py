import time

from src.database import api as database
from src.engine import criteria as criteria_engine
from src.engine import swap as swap_engine
from src.engine.chain import token as token_engine

def start(user_id, token_sniper_id):
  while True:
    token_sniper = database.get_token_sniper(user_id, token_sniper_id)
    if token_sniper:
      id, stage, chain, token, amount, slippage, wallet_id, criteria, stop_loss, auto_sell = token_sniper
      if stage == 'buy':
        if token_engine.check_liveness(chain, token):
          if criteria_engine.check(chain, token, criteria):
            swap_engine.buy(user_id, chain, token, amount, slippage, wallet_id, stop_loss)
            if len(auto_sell) == 0:
              database.remove_token_sniper(user_id, token_sniper_id)
            else:
              token_sniper['stage'] = 'sell'
              database.set_token_sniper(user_id, token_sniper_id, token_sniper)
          else:
            print('Cancel token sniper because of criteria')
      else:
        print('Auto Sell')
    else:
      break
    time.sleep(10)