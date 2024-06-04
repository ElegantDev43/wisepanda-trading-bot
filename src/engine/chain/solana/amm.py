
from solana.rpc.async_api import AsyncClient
import secrets
from eth_account import Account
from solana.rpc.api import Client
# Generate a new private key
import requests
import base64
import os
import base58
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solders import message
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Processed
import json


SWAP_URL = "https://quote-api.jup.ag/v6/swap"
WALLET_ADDRESS = "7L1scErJJSH7jBq61KVGpYGdyt7k9f5rzgBJoGSw2Vc9"
SOLANA_RPC_URL_ENDPOINT = "https://api.mainnet-beta.solana.com"

PRIVATE_KEY = Keypair.from_bytes(base58.b58decode(
    "2AuPc9wnuEDzGh3JbfWYGj6wuhLzGKq5rWc7YWiCXffmEhfNmdEqQaihM4bnZ4MuKHDnp6hkiQXutkmUwWd5SwL1"))


def market_order(type, token, amount, gas, slippage, wallets):
    private_key_b58 = os.getenv('PRIVATE_KEY')
    keypair = Keypair.from_base58_string(private_key_b58)
    user_public_key = keypair.pubkey()
    print(user_public_key)
    solana_rpc_url = 'https://api.mainnet-beta.solana.com'
    AMOUNT = 0
    if type == 0:
        INPUT_MINT = "So11111111111111111111111111111111111111112"
        OUTPUT_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        AMOUNT = int(float(amount) * 1000000000)
        SLIPPAGE = int(float(slippage) * 100)
        QUOTE_URL = f"https://quote-api.jup.ag/v6/quote?inputMint={
            INPUT_MINT}&outputMint={OUTPUT_MINT}&amount={AMOUNT}&slippageBps={SLIPPAGE}"
        print(QUOTE_URL)
        quote_response = requests.get(url=QUOTE_URL).json()
        payload = {
            "quoteResponse": quote_response,
            "userPublicKey": WALLET_ADDRESS,
            "wrapUnwrapSOL": True
        }
        # Get swap transaction route
        swap_route = requests.post(url=SWAP_URL, json=payload).json()[
            'swapTransaction']
        client = Client(endpoint=SOLANA_RPC_URL_ENDPOINT)

        # Decode and sign the transaction
        raw_transaction = VersionedTransaction.from_bytes(
            base64.b64decode(swap_route))
        signature = PRIVATE_KEY.sign_message(
            message.to_bytes_versioned(raw_transaction.message))
        signed_txn = VersionedTransaction.populate(
            raw_transaction.message, [signature])

        # Send the signed transaction
        opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
        result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)
        transaction_id = json.loads(result.to_json())['result']
        print(
            f"Transaction sent: https://explorer.solana.com/tx/{transaction_id}")

        return transaction_id

    elif type == 1:
        INPUT_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        OUTPUT_MINT = "So11111111111111111111111111111111111111112"
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenAccountsByOwner",
            "params": [
                WALLET_ADDRESS,
                {"mint": INPUT_MINT},
                {"encoding": "jsonParsed"}
            ]
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }
        total_balance = 0
        response = requests.post(solana_rpc_url, json=payload, headers=headers)
        if response.ok:
            result = response.json().get('result', {}).get('value', [])
            if result:
                # Loop through all accounts and sum the balances
                total_balance = sum(account['account']['data']['parsed']
                                    ['info']['tokenAmount']['uiAmount'] for account in result)
                print(f'Your balance for the token at address {
                      INPUT_MINT} is: {total_balance}')
            else:
                print('No token accounts found for the specified mint address.')
        else:
            print('Failed to fetch the balance.')
        AMOUNT = int(total_balance * 1000000 * amount / 100)
        SLIPPAGE = int(float(slippage) * 100)
        QUOTE_URL = f"https://quote-api.jup.ag/v6/quote?inputMint={
            INPUT_MINT}&outputMint={OUTPUT_MINT}&amount={AMOUNT}&slippageBps={SLIPPAGE}"
        print(QUOTE_URL)
        quote_response = requests.get(url=QUOTE_URL).json()
        payload = {
            "quoteResponse": quote_response,
            "userPublicKey": WALLET_ADDRESS,
            "wrapUnwrapSOL": True
        }
        # Get swap transaction route
        swap_route = requests.post(url=SWAP_URL, json=payload).json()[
            'swapTransaction']
        client = Client(endpoint=SOLANA_RPC_URL_ENDPOINT)

        # Decode and sign the transaction
        raw_transaction = VersionedTransaction.from_bytes(
            base64.b64decode(swap_route))
        signature = PRIVATE_KEY.sign_message(
            message.to_bytes_versioned(raw_transaction.message))
        signed_txn = VersionedTransaction.populate(
            raw_transaction.message, [signature])

        # Send the signed transaction
        opts = TxOpts(skip_preflight=False, preflight_commitment=Processed)
        result = client.send_raw_transaction(txn=bytes(signed_txn), opts=opts)
        print(result.to_json())
        transaction_id = json.loads(result.to_json())['result']
        print(
            f"Transaction sent: https://explorer.solana.com/tx/{transaction_id}")

        return transaction_id


def limit_order(type, token, amount, limit_token_price, tax, market_cap, liquidity,  wallets):
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    address = acct.address
    return address


def dca_order(type, token, amount, interval, duration, max_dca_price, min_dca_price, wallets):
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    address = acct.address
    return address
