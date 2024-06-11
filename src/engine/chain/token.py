from src.engine.chain.solana import token as solana
from src.engine.chain.ethereum import token as ethereum
from src.engine.chain.base import token as base

engines = [
  solana,
  ethereum,
  base
]

def get_metadata(chain, token):
  return engines[chain].get_metadata(token)

def check_liveness(chain, token):
  return engines[chain].check_liveness(token)

def get_market_data(chain, token):
  return engines[chain].get_market_data(token)