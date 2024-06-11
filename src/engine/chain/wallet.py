from src.engine.chain.solana import wallet as solana
from src.engine.chain.ethereum import wallet as ethereum
from src.engine.chain.base import wallet as base

engines = [
  solana,
  ethereum,
  base
]

def create_wallet(chain):
  return engines[chain].create_wallet()

def import_wallet(chain, private_key):
  return engines[chain].import_wallet(private_key)

def get_balance(chain, address):
  return engines[chain].get_balance(address)

def get_token_balance(chain, address, token):
  return engines[chain].get_token_balance(address, token)