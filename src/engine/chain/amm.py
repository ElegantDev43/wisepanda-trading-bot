from src.engine.chain.ethereum import amm as ethereum
from src.engine.chain.solana import amm as solana
from src.engine.chain.base import amm as base

chains = [
    ethereum,
    solana,
    base
]

def swap(chain_index, type, token, amount, gas, slippage, wallets):
    chains[chain_index].swap(type, token, amount, gas, slippage, wallets)