from src.engine.chain.ethereum import amm as ethereum
from src.engine.chain.solana import amm as solana
from src.engine.chain.base import amm as base

chains = [
    ethereum,
    solana,
    base
]


def market_order(chain_index, type, token, amount, gas, slippage, wallets):
    # time.sleep(10)
    tx_hash = chains[chain_index].market_order(
        type, token, amount, gas, slippage, wallets)
    return tx_hash


def limit_order(chain_index, thread_id, chat_id, type, token, amount, limit_token_price, tax, market_cap, liquidity, wallets):
    tx_hash = chains[chain_index].limit_order(thread_id, chat_id,
                                              type, token, amount, limit_token_price, tax, market_cap, liquidity,  wallets)
    return tx_hash


def dca_order(chain_index, thread_id, chat_id, type, token, amount, interval, duration, max_dca_price, min_dca_price, wallets):
    tx_hash = chains[chain_index].dca_order(
        thread_id, chat_id, type, token, amount, interval, duration, max_dca_price, min_dca_price,  wallets)
    return tx_hash
