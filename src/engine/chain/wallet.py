from src.engine.chain.ethereum import wallet as ethereum
from src.engine.chain.solana import wallet as solana
from src.engine.chain.base import wallet as base

chains = [
    ethereum,
    solana,
    base
]

def create_wallet(chain_index):
    return chains[chain_index].create_wallet()

def import_wallet(chain_index, private_key):
    return chains[chain_index].import_wallet(private_key)

def get_balance(chain_index, address):
    return chains[chain_index].get_balance(address)

def get_token_balance(chain_index, address, token):
    return chains[chain_index].get_token_balance(address, token)