import time
from threading import Thread

from src.database import api as database
from src.engine.chain import dex as dex_engine
from src.engine.chain import token as token_engine
from src.engine import stop_loss_engine

def buy(user_id, chain, token, amount, slippage, wallet_id, stop_loss):
  wallet = database.get_wallet(user_id, chain, wallet_id)
  print(wallet)
  transaction_id, amount = dex_engine.swap(chain, 'buy', token, amount, slippage, wallet)
  market_capital = token_engine.get_market_data(chain, token)['market_capital']
  position_id = time.time()
  position = {
    'id': position_id,
    'chain': chain,
    'token': token,
    'wallet_id': wallet_id,
    'transaction_id': transaction_id,
    'amount': amount,
    'market_capital': market_capital,
    'stop_loss':stop_loss
  }
  database.add_position(user_id, position)
  Thread(target=stop_loss_engine.start, args=(user_id, position_id)).start()
  return position

def sell(user_id, position_id, amount, slippage):
  position = database.get_position(user_id, position_id)
  wallet = database.get_wallet(user_id, position['chain'], position['wallet_id'])
  amount = int(position['amount'] * amount / 100)
  position['amount'] -= amount
  transaction_id, amount = dex_engine.swap(position['chain'], 'sell', position['token'], amount, slippage, wallet)
  if position['amount'] != 0:
    database.set_position(user_id, position_id, position)
  else:
    database.remove_position(user_id, position_id)
  return transaction_id, amount