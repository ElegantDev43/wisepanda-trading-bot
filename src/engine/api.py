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

def get_wallets(user_id, chain):
  return database.get_wallets(user_id, chain)

def create_wallet(user_id, chain):
  address, private_key = wallet_engine.create_wallet(chain)
  wallet = {
    'id': time.time(),
    'address': address,
    'private_key': private_key
  }
  database.add_wallet(user_id, chain, wallet)
  return wallet

def import_wallet(user_id, chain, private_key):
  address = wallet_engine.import_wallet(chain, private_key)
  wallet = {
    'id': time.time(),
    'address': address,
    'private_key': private_key
  }
  database.add_wallet(user_id, chain, wallet)
  return wallet

def remove_wallet(user_id, chain, wallet_id):
  database.remove_wallet(user_id, chain, wallet_id)

def market_buy(chain, token, amount, slippage, wallet):
  dex_engine.swap(chain, 'buy', token, amount, slippage, wallet)

def market_sell(chain, token, amount, slippage, wallet):
  dex_engine.swap(chain, 'sell', token, amount, slippage, wallet)

def get_token_snipers(user_id, chain):
  return database.get_token_snipers(user_id, chain)

def add_token_sniper(user_id, token_sniper):
  database.add_token_sniper(user_id, token_sniper)
  Thread(target=token_sniper_engine.start, args=(user_id, token_sniper['id'])).start()

def set_token_sniper(user_id, token_sniper_id, token_sniper):
  database.set_token_sniper(user_id, token_sniper_id, token_sniper)

def remove_token_sniper(user_id, token_sniper_id):
  database.remove_token_sniper(user_id, token_sniper_id)

def get_limit_orders(user_id, chain):
  return database.get_limit_orders(user_id, chain)

def add_limit_order(user_id, limit_order):
  database.add_limit_order(user_id, limit_order)
  Thread(target=limit_order_engine.start, args=(user_id, limit_order['id'])).start()

def set_limit_order(user_id, limit_order_id, limit_order):
  database.set_limit_order(user_id, limit_order_id, limit_order)

def remove_limit_order(user_id, limit_order_id):
  database.remove_limit_order(user_id, limit_order_id)

def get_dca_orders(user_id, chain):
  return database.get_dca_orders(user_id, chain)

def add_dca_order(user_id, dca_order):
  database.add_dca_order(user_id, dca_order)
  Thread(target=dca_order_engine.start, args=(user_id, dca_order['id'])).start()

def set_dca_order(user_id, dca_order_id, dca_order):
  database.set_dca_order(user_id, dca_order_id, dca_order)

def remove_dca_order(user_id, dca_order_id):
  database.remove_dca_order(user_id, dca_order_id)

def get_positions(user_id, chain):
  return database.get_positions(user_id, chain)