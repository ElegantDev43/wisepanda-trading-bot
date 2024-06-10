from base58 import b58decode
from solana.rpc.core import RPCException
import os
from web3 import Web3
import requests
from solana.rpc.api import Client
from solders.pubkey import Pubkey


def get_name(token):
    web3 = Web3(Web3.HTTPProvider(os.getenv('ETHEREUM_RPC_URL')))
    token_address = Web3.to_checksum_address(token)
    token_abi = [
        {
            "constant": True,
            "inputs": [],
            "name": "name",
            "outputs": [{"name": "", "type": "string"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function"
        }
    ]
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    token_name = token_contract.functions.name().call()
    return token_name


def check_liveness(token_address):

    return 0


def get_information(token):
    price = get_token_price()
    market_cap = get_solana_market_cap()
    details = {'price': price, 'market_cap': market_cap}
    token_address = "8XSixRF5p2Hv96UEnX8ggzkCQY4r9QytumkCL3PkuXEx"
    data = get_token_metadata(token_address)
    liquidity = get_liquidity()
    print(liquidity)
    return details


def get_token_metadata(token_address):

    client = Client("https://api.mainnet-beta.solana.com")
    # Convert the base-58 encoded string to binary
    binary_address = b58decode(token_address)

    account_info = client.get_account_info(Pubkey(binary_address))
    return account_info


def get_token_price():
    url = 'https://quote-api.jup.ag/v6/quote'
    params = {
        'inputMint': 'So11111111111111111111111111111111111111112',
        'outputMint': 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
        'amount': '100000',
        'slippageBps': '50'
    }
    try:
        response = requests.get(url, params=params)
        quoteResponse = response.json()
        return float(quoteResponse['outAmount']) / 100.0
    except Exception as e:
        print("Error fetching quote:", e)


def get_solana_market_cap():
    url = 'https://api.coingecko.com/api/v3/coins/solana'
    response = requests.get(url)
    data = response.json()
    market_cap = data['market_data']['market_cap']['usd']
    return market_cap


def get_liquidity():
    solana_rpc_url = "https://api.mainnet-beta.solana.com"
# Define the liquidity pool address (replace with actual pool address)
    pool_address = "AaGF7g7GKrH6j7iVvC2kSB2vygQ2wP7m6pQJga6TPkaQ"

    # Get token accounts by owner (the liquidity pool address)
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccountsByOwner",
        "params": [
            pool_address,
            {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
            {"encoding": "jsonParsed"}
        ]
    }

    response = requests.post(solana_rpc_url, json=payload)
    token_accounts = response.json()
    # Calculate the liquidity by summing up the token amounts
    liquidity = 0

    for account in token_accounts['result']['value']:
        amount = int(account['account']['data']['parsed']
                     ['info']['tokenAmount']['amount'])
        liquidity += amount
    return liquidity
