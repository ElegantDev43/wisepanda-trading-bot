import os

from src.engine.chain import wallet as wallet_engine
from src.engine.chain import token as token_engine

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
  name = token_engine.get_name(chain_index, token)
  print('name', name)

  liveness = token_engine.check_liveness(chain_index, token)
  print('liveness', liveness)

  if not liveness:
    return

  information = token_engine.get_information(chain_index, token)
  print('information', information)

def initialize():
  check_wallet_engine()
  check_token_engine()