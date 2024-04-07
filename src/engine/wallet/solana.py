# from solana.account import Account
# from solana.publickey import PublicKey
from solana.rpc.api import Client

import config

solana_client = Client(config.SOLANA_RPC_URL)

def create_wallet():
    account = Account()
    address = str(account.public_key())
    private_key = account.secret_key()
    return address, private_key

def import_wallet(private_key):
    account = Account(private_key)
    address = str(account.public_key())
    public_key = PublicKey(address)
    balance = solana_client.get_balance(public_key)
    return address, balance
