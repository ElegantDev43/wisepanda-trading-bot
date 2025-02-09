from src.engine.chain.ethereum import amm as ethereum
from src.engine.chain.solana import amm as solana
from src.engine.chain.base import amm as base

chains = [
    ethereum,
    solana,
    base
]

def market_order(chain_index, type, token, amount, gas, slippage, wallets):
    chains[chain_index].market_order(type, token, amount, gas, slippage, wallets)