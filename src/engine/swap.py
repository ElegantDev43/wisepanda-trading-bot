import time

from src.database import api as database
from src.engine.chain import dex as dex_engine

def buy(user_id, chain, token, amount, slippage, wallet_id):
  wallet = database.get_wallet(user_id, chain, wallet_id)
  transaction_id, amount = dex_engine.swap(chain, 'buy', token, amount, slippage, wallet)
  position = {
    'id': time.time(),
    'chain': chain,
    'token': token,
    'wallet_id': wallet_id,
    'transaction_id': transaction_id,
    'amount': amount,
  }
  database.add_position(user_id, position)
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