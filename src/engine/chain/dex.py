from src.engine.chain.solana import dex as solana
from src.engine.chain.ethereum import dex as ethereum
from src.engine.chain.base import dex as base

engines = [
  solana,
  ethereum,
  base
]

def swap(chain, type, token, amount, slippage, wallet):
  return engines[chain].swap(type, token, amount, slippage, wallet)