import os

from src.engine.chain import wallet as wallet_engine
from src.engine.chain import token as token_engine
from src.engine.chain import dex as dex_engine

chain_index = 0
token = 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'

def check_wallet_engine():
  address, private_key = wallet_engine.create_wallet(chain_index)
  print('address', address)
  print('private_key', private_key)

  address = wallet_engine.import_wallet(chain_index, private_key)
  print('address', address)

  balance = wallet_engine.get_balance(chain_index, address)
  print('balance', balance)

  token_balance = wallet_engine.get_token_balance(chain_index, address, token)
  print('token_balance', token_balance)

def check_token_engine():
  metadata = token_engine.get_metadata(chain_index, token)
  print('metadata', metadata)

  liveness = token_engine.check_liveness(chain_index, token)
  print('liveness', liveness)

  if not liveness:
    return

  information = token_engine.get_market_data(chain_index, token)
  print('information', information)

def check_dex_engine():
  amount = int(3 * 1_000_000)
  wallet = {
    'address': '7L1scErJJSH7jBq61KVGpYGdyt7k9f5rzgBJoGSw2Vc9',
    'private_key': '2AuPc9wnuEDzGh3JbfWYGj6wuhLzGKq5rWc7YWiCXffmEhfNmdEqQaihM4bnZ4MuKHDnp6hkiQXutkmUwWd5SwL1'
  }
  dex_engine.swap(chain_index, 'buy', token, amount, None, wallet)

def initialize():
  # check_wallet_engine()
  check_token_engine()
  # check_dex_engine()
  print('Test Done')