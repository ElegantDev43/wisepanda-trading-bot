from solders.keypair import Keypair # type: ignore
from solders.signature import Signature # type: ignore
from solana.rpc.api import Client
import json
import requests
from src.engine.chain.solana.solana_tracker.solanatracker import SolanaTracker
from src.engine.chain.solana.token import get_metadata

from src.engine.chain import token as token_engine
from src.engine import api as main_api
client = Client("https://rpc.solanatracker.io/public?advancedTx=true")

def swap(type, token, amount, slippage, wallet):
  sol = "So11111111111111111111111111111111111111112"
  if type == 'buy':
    inputMint = sol
    outputMint = token
    decimals = 9
  else:
    inputMint = token
    outputMint = sol
    decimals = token_engine.get_metadata(0, token)['decimals']
  
  amount = float(amount / 10**decimals)
  keypair = Keypair.from_base58_string(wallet['private_key'])

  solana_tracker = SolanaTracker(keypair, "https://rpc.solanatracker.io/public?advancedTx=true")

  swap_response = solana_tracker.get_swap_instructions(
    inputMint,
    outputMint,
    amount,
    slippage,
    str(keypair.pubkey()),
    0.00005,
    True
  )

  txid = solana_tracker.perform_swap(swap_response)

  if not txid:
    raise Exception("Swap failed")

  print("Transaction ID:", txid)
  print("Transaction URL:", f"https://explorer.solana.com/tx/{txid}")
  
  
  api_key = "IbPGi3HgfdZdUcM7"
  txn_signature = txid
  network = "mainnet-beta"

  url = f"https://api.shyft.to/sol/v1/transaction/parsed?network={network}&txn_signature={txn_signature}"

  headers = {
      "x-api-key": api_key
  }
  response = requests.get(url, headers=headers)
  exact_amount = 0
  if response.status_code == 200:
      result = response.json()
      # Extract the 'out' amount from the JSON response
      try:
          actions = result['result']['actions']
          for action in actions:
              if 'info' in action and 'tokens_swapped' in action['info']:
                  out_amount = action['info']['tokens_swapped']['out']['amount']
                  exact_amount = out_amount * 10 ** get_metadata(outputMint)['decimals']
                  break
      except KeyError as e:
          print(f"KeyError: {e} - The key was not found in the JSON response.")
  else:
      print("Error:", response.status_code, response.text)
  return txid, exact_amount