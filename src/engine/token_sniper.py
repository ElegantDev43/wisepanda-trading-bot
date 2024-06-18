import time

from src.database import api as database

from src.engine.chain import token as token_engine
from src.engine.chain import dex as dex_engine

def start(user_id, token_sniper_id):
  while True:
    token_sniper = database.get_token_sniper(user_id, token_sniper_id)
    if token_sniper:
      stage, chain, token, amount, slippage, wallet_id, criteria, stop_loss, auto_sell = token_sniper
      if stage == 'buy':
        if token_engine.check_liveness(chain, token):
          max_price = criteria
          price = token_engine.get_market_data(chain, token)
          valid = price < max_price
          if valid:
            wallet = database.get_wallet(user_id, chain, wallet_id)
            dex_engine.swap(chain, 'buy', token, amount, slippage, wallet)
          else:
            print('Cancel token sniper because of criteria')
      else:
        print('Auto Sell')
    else:
      break
    time.sleep(10)