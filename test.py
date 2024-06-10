import os

from src.engine.chain import wallet

chain_index = 0

def check_wallet_engine():
  address, private_key = wallet.create_wallet(chain_index)
  print('address', address)
  print('private_key', private_key)

  address = wallet.import_wallet(chain_index, private_key)
  print('address', address)

  balance = wallet.get_balance(chain_index, address)
  print('balance', balance)

def initialize():
  check_wallet_engine()