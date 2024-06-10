from src.engine.chain.solana import dex as solana
from src.engine.chain.ethereum import dex as ethereum
from src.engine.chain.base import dex as base

chains = [
  solana,
  ethereum,
  base
]

def swap(chain_index, type, token, amount, slippage, wallet):
  chains[chain_index].swap(type, token, amount, slippage, wallet)