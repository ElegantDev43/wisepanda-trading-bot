from web3 import Web3

import config
from engine.amm import uniswap

def get_token_name(token):
    web3 = Web3(Web3.HTTPProvider(config.ETHEREUM_RPC_URL))
    token_address = token
    token_abi = [
        {
            "constant": True,
            "inputs": [],
            "name": "name",
            "outputs": [{"name": "", "type": "string"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        }
    ]
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    token_name = token_contract.functions.name().call()
    return token_name

def check_token_liveness(token):
    return uniswap.check_token_liveness(token)

def get_token_exchange_data(token):
    return uniswap.get_token_exchange_data(token)

def create_order(user, token, type, side, amount, wallets):
    uniswap.create_order(user, token, type, side, amount, wallets)
