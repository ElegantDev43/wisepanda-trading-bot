import os
from web3 import Web3
import requests

# import config


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


def check_liveness(token):
    try:
        query = """
        {
            pools(
                where: {
                    token0: "%s"
                    token1: "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
                }
            ) {
                id
            }
        }
        """ % token.lower()
        response = requests.post(
            'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3', json={'query': query})
        data = response.json()
        token_exists = bool(data.get('data', {}).get('pools'))
        return token_exists
    except Exception as e:
        print("Error:", e)
        return False


def get_information(token):
    try:
        query = """
        {
            pools(
                where: {
                    token0: "%s"
                    token1: "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
                }
            ) {
                id
                liquidity
                txCount
                volumeUSD
                totalValueLockedUSD
                token0 {
                    id
                    symbol
                    totalSupply
                    volumeUSD
                    txCount
                    totalValueLockedUSD
                }
                token1 {
                    id
                    symbol
                }
            }
        }
        """ % token.lower()
        response = requests.post(
            'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3', json={'query': query})
        data = response.json()
        return data.get('data', {}).get('pools', [])[0]
    except Exception as e:
        print("Error:", e)
        return False
