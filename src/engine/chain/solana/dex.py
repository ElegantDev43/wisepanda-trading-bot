import os
import requests
import json
import base64

from solana.rpc.api import Client
from solana.rpc.types import TxOpts

from solders.message import to_bytes_versioned # type: ignore
from solders.keypair import Keypair # type: ignore
from solders.transaction import VersionedTransaction # type: ignore

def swap(type, token, amount, slippage, wallet):
  try:
    sol = 'So11111111111111111111111111111111111111112'
    if type == 'buy':
      input_mint = sol
      output_mint = token
    else:
      input_mint = token
      output_mint = sol

    url = "https://quote-api.jup.ag/v6/quote"
    headers = {
      'Accept': 'application/json'
    }
    payload = {
      'inputMint': input_mint,
      'outputMint': output_mint,
      'amount': amount,
      'slippageBps': int(slippage * 100)
    }
    response = requests.request("GET", url, headers=headers, params=payload)
    quote_response = response.json()

    # print('quote_response', quote_response)

    url = "https://quote-api.jup.ag/v6/swap"
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
    payload = {
        'userPublicKey': wallet['address'],
        'quoteResponse': quote_response
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    swap_response = response.json()

    # print('swap_response', swap_response)

    swap_transaction = swap_response['swapTransaction']
    transaction_bytes = base64.b64decode(swap_transaction)
    transaction = VersionedTransaction.from_bytes(transaction_bytes)

    sender = Keypair.from_base58_string(wallet['private_key'])
    signature = sender.sign_message(to_bytes_versioned(transaction.message))
    transaction = transaction.populate(transaction.message, [signature])

    client = Client(os.getenv('SOLANA_RPC_URL'))
    opts = TxOpts(skip_preflight=True, max_retries=3)
    result = client.send_raw_transaction(bytes(transaction), opts)
    transaction_id = json.loads(result.to_json())['result']
    print('transaction_id', transaction_id)
    return transaction_id

  except Exception as e:
    print(f"An unexpected error occurred: {e}")
    return None