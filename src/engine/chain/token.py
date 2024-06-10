from src.engine.chain.solana import token as solana
from src.engine.chain.ethereum import token as ethereum
from src.engine.chain.base import token as base

chains = [
  solana,
  ethereum,
  base
]

def get_name(chain_index, token):
  return chains[chain_index].get_name(token)

def check_liveness(chain_index, token):
  return chains[chain_index].check_liveness(token)

def get_information(chain_index, token):
  return chains[chain_index].get_information(token)