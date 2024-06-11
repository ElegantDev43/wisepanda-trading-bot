import time

from src.database import api as database

from src.engine.chain import token as token_engine
from src.engine.chain import dex as dex_engine

def start(chat_id, chain_index, timestamp):
  while True:
    token_sniper = database.get_token_sniper(chat_id, chain_index, timestamp)
    if token_sniper:
      stage, token, amount, slippage, wallet_index, criteria = token_sniper
      if stage == 'buy':
        if token_engine.check_liveness(chain_index, token):
          max_price = criteria
          price = token_engine.get_market_data(chain_index, token)
          valid = price < max_price
          if valid:
            dex_engine.swap(chain_index, 'buy', token, amount, slippage, wallet_index)
          else:
            print('Cancel token sniper because of criteria')
          break
    else:
      break
    time.sleep(10)