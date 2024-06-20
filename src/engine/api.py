import time
from threading import Thread

from src.database import api as database

from src.engine import token_sniper as token_sniper_engine
from src.engine import limit_order as limit_order_engine
from src.engine import dca_order as dca_order_engine

from src.engine.chain import wallet as wallet_engine
from src.engine.chain import token as token_engine
from src.engine.chain import dex as dex_engine

def add_user(user_id):
  database.add_user(user_id)

def get_user(user_id):
  return database.get_user(user_id)

def get_chains():
  return [
    'solana',
    'ethereum',
    'base'
  ]

def get_chain(user_id):
  return database.get_chain(user_id)

def set_chain(user_id, chain):
  database.set_chain(user_id, chain)

def get_wallets(user_id):
  chain = get_chain(user_id)
  return database.get_wallets(user_id, chain)

def get_wallet_balance(user_id, wallet_id):
  chain = get_chain(user_id)
  wallet = database.get_wallet(user_id, chain, wallet_id)
  address = wallet['address']
  return wallet_engine.get_balance(chain, address)

def create_wallet(user_id, wallet_name):
  chain = get_chain(user_id)
  address, private_key = wallet_engine.create_wallet(chain)
  wallet = {
    'id': time.time(),
    'name': wallet_name,
    'address': address,
    'private_key': private_key
  }
  database.add_wallet(user_id, chain, wallet)
  return wallet

def import_wallet(user_id, private_key, wallet_name):
  chain = get_chain(user_id)
  address = wallet_engine.import_wallet(chain, private_key)
  wallet = {
    'id': time.time(),
    'name': wallet_name,
    'address': address,
    'private_key': private_key
  }
  database.add_wallet(user_id, chain, wallet)
  return wallet

def remove_wallet(user_id, wallet_id):
  chain = get_chain(user_id)
  database.remove_wallet(user_id, chain, wallet_id)

def get_token_metadata(user_id, token):
  chain = get_chain(user_id)
  return token_engine.get_metadata(chain, token)

def get_token_market_data(user_id, token):
  chain = get_chain(user_id)
  return token_engine.get_market_data(chain, token)

def get_positions(user_id):
  chain = get_chain(user_id)
  return database.get_positions(user_id, chain)

def market_buy(user_id, token, amount, slippage, wallet_id):
  chain = get_chain(user_id)
  wallet = database.get_wallet(user_id, chain, wallet_id)
  result = dex_engine.swap(chain, 'buy', token, amount, slippage, wallet)
  position = {
    'chain': chain,
    'token': token,
    'amount': {
      'in': amount,
      'out': result
    },
    'wallet_id': wallet_id
  }
  database.add_position(user_id, position)
  return position

def market_sell(user_id, position_id, amount, slippage):
  position = database.get_position(position_id)
  wallet = database.get_wallet(user_id, position['chain'], position['wallet_id'])
  result = dex_engine.swap(position['chain'], 'sell', position['token'], amount, slippage, wallet)
  if amount != position['amount']['out']:
    position['amount'] = {
      'in': position['amount']['in'] - result,
      'out': position['amount']['out'] - amount
    }
    database.set_position(user_id, position_id, position)
  else:
    database.remove_position(user_id, position_id)

def get_token_snipers(user_id):
  chain = get_chain(user_id)
  return database.get_token_snipers(user_id, chain)

def add_token_sniper(user_id, token, amount, slippage, wallet_id, criteria, stop_loss, auto_sell):
  chain = get_chain(user_id)
  token_sniper = {
    'id': time.time(),
    'stage': 'buy',
    'chain': chain,
    'token': token,
    'amount': amount,
    'slippage': slippage,
    'wallet_id': wallet_id,
    'criteria': criteria,
    'stop_loss': stop_loss,
    'auto_sell': auto_sell
  }
  database.add_token_sniper(user_id, token_sniper)
  Thread(target=token_sniper_engine.start, args=(user_id, token_sniper['id'])).start()

def set_token_sniper(user_id, token_sniper_id, token_sniper):
  database.set_token_sniper(user_id, token_sniper_id, token_sniper)

def remove_token_sniper(user_id, token_sniper_id):
  database.remove_token_sniper(user_id, token_sniper_id)

def get_limit_orders(user_id):
  chain = get_chain(user_id)
  return database.get_limit_orders(user_id, chain)

def add_limit_order(user_id, type, token, amount, slippage, wallet_id, criteria):
  chain = get_chain(user_id)
  limit_order = {
    'id': time.time(),
    'chain': chain,
    'type': type,
    'token': token,
    'amount': amount,
    'slippage': slippage,
    'wallet_id': wallet_id,
    'criteria': criteria
  }
  database.add_limit_order(user_id, limit_order)
  Thread(target=limit_order_engine.start, args=(user_id, limit_order['id'])).start()

def set_limit_order(user_id, limit_order_id, limit_order):
  database.set_limit_order(user_id, limit_order_id, limit_order)

def remove_limit_order(user_id, limit_order_id):
  database.remove_limit_order(user_id, limit_order_id)

def get_dca_orders(user_id):
  chain = get_chain(user_id)
  return database.get_dca_orders(user_id, chain)

def add_dca_order(user_id, type, token, amount, slippage, wallet_id, criteria, interval, count):
  chain = get_chain(user_id)
  dca_order = {
    'id': time.time(),
    'chain': chain,
    'type': type,
    'token': token,
    'amount': amount,
    'slippage': slippage,
    'wallet_id': wallet_id,
    'criteria': criteria,
    'interval': interval,
    'count': count
  }
  database.add_dca_order(user_id, dca_order)
  Thread(target=dca_order_engine.start, args=(user_id, dca_order['id'])).start()

def set_dca_order(user_id, dca_order_id, dca_order):
  database.set_dca_order(user_id, dca_order_id, dca_order)

def remove_dca_order(user_id, dca_order_id):
  database.remove_dca_order(user_id, dca_order_id)
  
def set_auto_order(user_id):
  database.set_auto_order(user_id)
  
def unset_auto_order(user_id):
  database.unset_auto_order(user_id)