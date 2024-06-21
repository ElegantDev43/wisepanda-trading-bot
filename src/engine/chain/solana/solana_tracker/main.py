from solders.keypair import Keypair # type: ignore
from solders.signature import Signature # type: ignore
from solana.rpc.api import Client
import json

from src.engine.chain.solana.solana_tracker.solanatracker import SolanaTracker

from src.engine.chain import token as token_engine

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
    decimals = token_engine.get_metadata(token)['decimals']
  
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

  signature = Signature.from_string(txid)
  transaction_json = client.get_transaction(signature).to_json()

  transaction_data = json.loads(transaction_json)

  pre_token_balances = transaction_data['result']['meta']['preTokenBalances']
  post_token_balances = transaction_data['result']['meta']['postTokenBalances']

  def find_balance_difference(pre_balances, post_balances, account_index):
    pre_balance = next((item for item in pre_balances if item['accountIndex'] == account_index), None)
    post_balance = next((item for item in post_balances if item['accountIndex'] == account_index), None)

    if pre_balance and post_balance:
      pre_amount = float(pre_balance['uiTokenAmount']['uiAmount'])
      post_amount = float(post_balance['uiTokenAmount']['uiAmount'])
      return post_amount - pre_amount
    return None
  
  account_index = 5
  exact_amount = find_balance_difference(pre_token_balances, post_token_balances, account_index)
  print(exact_amount)
  return txid, exact_amount