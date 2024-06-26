import time
from threading import Thread

from src.database import api as database

from src.engine import token_sniper as token_sniper_engine
from src.engine import lp_sniper as lp_sniper_engine
from src.engine import limit_order as limit_order_engine
from src.engine import dca_order as dca_order_engine

from src.engine import swap as swap_engine
from src.engine.swing import api as swing_engine

from src.engine.chain import wallet as wallet_engine
from src.engine.chain import token as token_engine

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

def get_wallet_balance(user_id, wallet_id):
  chain = get_chain(user_id)
  wallet = database.get_wallet(user_id, chain, wallet_id)
  address = wallet['address']
  return wallet_engine.get_balance(chain, address)

def is_valid_token(user_id, token):
  chain = get_chain(user_id)
  return token_engine.is_valid(chain, token)

def get_token_metadata(user_id, token):
  chain = get_chain(user_id)
  return token_engine.get_metadata(chain, token)

def check_token_liveness(user_id, token):
  chain = get_chain(user_id)
  return token_engine.check_liveness(chain, token)

def get_token_market_data(user_id, token):
  chain = get_chain(user_id)
  return token_engine.get_market_data(chain, token)

def market_buy(user_id, token, amount, slippage, wallet_id):
  chain = get_chain(user_id)
  return swap_engine.buy(user_id, chain, token, amount, slippage, wallet_id)

def market_sell(user_id, position_id, amount, slippage):
  return swap_engine.sell(user_id, position_id, amount, slippage)

def get_positions(user_id):
  chain = get_chain(user_id)
  return database.get_positions(user_id, chain)

def get_auto_sniper(user_id):
  chain = get_chain(user_id)
  return database.get_auto_sniper(user_id, chain)

def set_auto_sniper(user_id, auto_sniper):
  chain = get_chain(user_id)
  database.set_auto_sniper(user_id, chain, auto_sniper)

def get_token_snipers(user_id):
  chain = get_chain(user_id)
  return database.get_token_snipers(user_id, chain)

def add_token_sniper(user_id, token, amount, slippage, wallet_id, auto_sell):
  chain = get_chain(user_id)
  token_sniper = {
    'id': time.time(),
    'stage': 'buy',
    'chain': chain,
    'token': token,
    'amount': amount,
    'slippage': slippage,
    'wallet_id': wallet_id,
    'auto_sell': auto_sell
  }
  database.add_token_sniper(user_id, token_sniper)
  Thread(target=token_sniper_engine.start, args=(user_id, token_sniper['id'])).start()

def set_token_sniper(user_id, token_sniper_id, token_sniper):
  database.set_token_sniper(user_id, token_sniper_id, token_sniper)

def remove_token_sniper(user_id, token_sniper_id):
  database.remove_token_sniper(user_id, token_sniper_id)

def get_lp_snipers(user_id):
  chain = get_chain(user_id)
  return database.get_lp_snipers(user_id, chain)

def add_lp_sniper(user_id, token, amount, slippage, wallet_id):
  chain = get_chain(user_id)
  lp_sniper = {
    'id': time.time(),
    'stage': 'buy',
    'chain': chain,
    'token': token,
    'amount': amount,
    'slippage': slippage,
    'wallet_id': wallet_id
  }
  database.add_lp_sniper(user_id, lp_sniper)
  Thread(target=lp_sniper_engine.start, args=(user_id, lp_sniper['id'])).start()

def set_lp_sniper(user_id, lp_sniper_id, lp_sniper):
  database.set_lp_sniper(user_id, lp_sniper_id, lp_sniper)

def remove_lp_sniper(user_id, lp_sniper_id):
  database.remove_lp_sniper(user_id, lp_sniper_id)

def get_limit_orders(user_id):
  chain = get_chain(user_id)
  return database.get_limit_orders(user_id, chain)

def add_limit_buy(user_id, token, amount, slippage, wallet_id, max_market_capital):
  chain = get_chain(user_id)
  limit_order = {
    'id': time.time(),
    'type': 'buy',
    'chain': chain,
    'token': token,
    'amount': amount,
    'slippage': slippage,
    'wallet_id': wallet_id,
    'max_market_capital': max_market_capital
  }
  database.add_limit_order(user_id, limit_order)
  Thread(target=limit_order_engine.start, args=(user_id, limit_order['id'])).start()

def add_limit_sell(user_id, position_id, amount, slippage, profit):
  limit_order = {
    'id': time.time(),
    'type': 'sell',
    'position_id': position_id,
    'amount': amount,
    'slippage': slippage,
    'profit': profit
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

def add_dca_buy(user_id, token, amount, slippage, wallet_id, interval, count):
  chain = get_chain(user_id)
  dca_order = {
    'id': time.time(),
    'type': 'buy',
    'chain': chain,
    'token': token,
    'amount': amount,
    'slippage': slippage,
    'wallet_id': wallet_id,
    'interval': interval,
    'count': count,
  }
  database.add_dca_order(user_id, dca_order)
  Thread(target=dca_order_engine.start, args=(user_id, dca_order['id'])).start()

def add_dca_sell(user_id, position_id, amount, slippage, interval, count):
  dca_order = {
    'id': time.time(),
    'type': 'sell',
    'position_id': position_id,
    'amount': amount,
    'slippage': slippage,
    'interval': interval,
    'count': count
  }
  database.add_dca_order(user_id, dca_order)
  Thread(target=dca_order_engine.start, args=(user_id, dca_order['id'])).start()

def set_dca_order(user_id, dca_order_id, dca_order):
  database.set_dca_order(user_id, dca_order_id, dca_order)

def remove_dca_order(user_id, dca_order_id):
  database.remove_dca_order(user_id, dca_order_id)

def get_auto_order(user_id):
  chain = get_chain(user_id)
  return database.get_auto_order(user_id, chain)

def set_auto_order(user_id, auto_order):
  chain = get_chain(user_id)
  database.set_auto_order(user_id, chain, auto_order)

def get_auto_swing(user_id):
  if swing_engine.SetFullyAutoTokens('Auto Status',user_id) == 'Stop':
    profit, original_amount, wallet_id = swing_engine.SetFullyAutoTokens('Market Status',user_id)
    return 'Active', profit, original_amount,wallet_id
  else:
    return 'DeActive'

def start_auto_swing(user_id, amount, wallet_id):
  chain = get_chain(user_id)
  wallet = database.get_wallet(user_id, chain, wallet_id)
  swing_engine.SetFullyAutoTokens('Start', user_id, amount, wallet)

def stop_auto_swing(user_id):
  swing_engine.SetFullyAutoTokens('Stop', user_id)

def get_price_chart(token):
  return swing_engine.getTokenImage(token)