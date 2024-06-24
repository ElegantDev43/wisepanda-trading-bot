import requests
import os
import json
from solders.keypair import Keypair # type: ignore

def create_wallet():
  keypair = Keypair()
  address = str(keypair.pubkey())
  private_key = str(keypair)
  return address, private_key

def import_wallet(private_key):
  keypair = Keypair.from_base58_string(private_key)
  address = str(keypair.pubkey())
  return address

def get_balance(address):
  headers = { 'Content-Type': 'application/json' }
  payload = json.dumps({
    'jsonrpc': '2.0',
    'id': 1,
    'method': 'getBalance',
    'params':  [address]
  })
  response = requests.post(os.getenv('SOLANA_RPC_URL'), headers=headers, data=payload)
  response_json = response.json()
  if 'result' in response_json:
    lamports = response_json['result']['value']
    return lamports
  else:
    error_message = response_json.get('error', {}).get('message', 'Unknown error')
    raise Exception(f'Failed to retrieve balance: {error_message}')