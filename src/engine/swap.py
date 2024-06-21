import time

from src.database import api as database
from src.engine.chain import dex as dex_engine

def buy(user_id, chain, token, amount, slippage, wallet_id, stop_loss):
  wallet = database.get_wallet(user_id, chain, wallet_id)
  txid, output = dex_engine.swap(chain, 'buy', token, amount, slippage, wallet)
  position = {
    'id': time.time(),
    'chain': chain,
    'token': token,
    'amount': {
      'in': amount,
      'out': output
    },
    'wallet_id': wallet_id,
    'stop_loss': stop_loss
  }
  database.add_position(user_id, position)
  return txid, output

def sell(user_id, position_id, amount, slippage):
  position = database.get_position(user_id,position_id)
  wallet = database.get_wallet(user_id, position['chain'], position['wallet_id'])
  amount = int(position['amount']['out'] * amount / 100)
  txid, output = dex_engine.swap(position['chain'], 'sell', position['token'], amount, slippage, wallet)
  if amount != position['amount']['out']:
    position['amount'] = {
      'in': position['amount']['in'] - output,
      'out': position['amount']['out'] - amount
    }
    database.set_position(user_id, position_id, position)
  else:
    database.remove_position(user_id, position_id)
  return txid, output