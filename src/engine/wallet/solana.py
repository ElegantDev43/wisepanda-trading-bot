from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
from base58 import b58encode, b58decode
import requests

import config

def create_wallet():
    ed25519_private_key = Ed25519PrivateKey.generate()
    public_key = ed25519_private_key.public_key()
    public_key_bytes = public_key.public_bytes(encoding=Encoding.Raw, format=PublicFormat.Raw)
    address = b58encode(public_key_bytes).decode("utf-8")
    private_key_bytes = ed25519_private_key.private_bytes(encoding=Encoding.Raw, format=PrivateFormat.Raw, encryption_algorithm=NoEncryption())
    private_key = b58encode(private_key_bytes).decode("utf-8")
    return address, private_key

def import_wallet(private_key):
    private_key_bytes = b58decode(private_key)
    ed25519_private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)
    public_key = ed25519_private_key.public_key()
    public_key_bytes = public_key.public_bytes(encoding=Encoding.Raw, format=PublicFormat.Raw)
    address = b58encode(public_key_bytes).decode("utf-8")
    balance = get_balance(address)
    return address, balance

def get_balance(address):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [address]
    }
    response = requests.post(config.SOLANA_RPC_URL, json=payload)
    response_json = response.json()

    if 'error' in response_json:
        raise Exception(f"Error occurred: {response_json['error']}")

    balance = response_json['result']['value']
    return balance

def get_token_balance(address, token):
    return address, token
