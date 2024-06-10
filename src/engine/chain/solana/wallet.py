from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
from base58 import b58encode, b58decode
import requests
import os
import base58
import json
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey


def create_wallet():
    keypair = Keypair()
    address = str(keypair.pubkey())
    private_key = str(keypair)
    return address, private_key


def import_wallet(private_key):
    keypair = Keypair.from_base58_string(private_key)
    address = str(keypair.pubkey())
    balance = get_balance(address)
    # print(balance)
    return address, balance


def get_balance(address):
    url = "https://api.mainnet-beta.solana.com"

    # JSON payload for the request
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params":  [address]
    })

    # Headers
    headers = {
        "Content-Type": "application/json"
    }

    # Send the request
    response = requests.post(url, headers=headers, data=payload)

    # Parse the JSON response
    response_json = response.json()

    if 'result' in response_json:
        lamports = response_json['result']['value']
        # Convert lamports to SOL (1 SOL = 1,000,000,000 lamports)
        sol = lamports / 1_000_000_000
        return sol
    else:
        error_message = response_json.get(
            "error", {}).get("message", "Unknown error")
        raise Exception(f"Failed to retrieve balance: {error_message}")
