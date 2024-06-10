from src.engine.chain.ethereum import hot as ethereum
from src.engine.chain.solana import hot as solana
from src.engine.chain.base import hot as base

chains = [
    ethereum,
    solana,
    base
]

def get(chain_index):
    return chains[chain_index].get()