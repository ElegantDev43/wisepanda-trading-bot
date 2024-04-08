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
    balance = get_balance(balance)
    return address, balance

def get_balance(address):
    web3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{config.INFURA_PROJECT_ID}'))
    checksum_address = Web3.to_checksum_address(address)
    balance_wei = web3.eth.get_balance(checksum_address)
    balance = web3.from_wei(balance_wei, 'ether')
    return balance