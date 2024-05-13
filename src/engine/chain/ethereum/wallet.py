from eth_account import Account
from eth_keys import keys
from web3 import Web3

import config

def create_wallet():
    account = Account.create()
    address = account.address
    private_key = account._private_key.hex()[2:]
    return address, private_key

def import_wallet(private_key):
    eth_key = keys.PrivateKey(bytes.fromhex(private_key))
    address = eth_key.public_key.to_checksum_address()
    return address

def get_balance(address):
    web3 = Web3(Web3.HTTPProvider(config.ETHEREUM_RPC_URL))
    balance_wei = web3.eth.get_balance(address)
    balance = web3.from_wei(balance_wei, 'ether')
    return balance

def get_token_balance(address, token):
    web3 = Web3(Web3.HTTPProvider(config.ETHEREUM_RPC_URL))
    token_abi = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function",
        }
    ]
    contract = web3.eth.contract(address=token, abi=token_abi)
    balance = contract.functions.balanceOf(address).call()
    return balance
