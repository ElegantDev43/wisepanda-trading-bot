from eth_account import Account
from eth_keys import keys

def create_wallet():
    account = Account.create()
    address = account.address
    private_key = account._private_key.hex()[2:]
    return address, private_key

def get_address(private_key):
    eth_key = keys.PrivateKey(bytes.fromhex(private_key))
    address = eth_key.public_key.to_checksum_address()
    return address