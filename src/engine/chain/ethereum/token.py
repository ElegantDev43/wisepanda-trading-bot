import os
from web3 import Web3
import requests

# import config
web3 = Web3(Web3.HTTPProvider(
    'https://mainnet.infura.io/v3/391b9518dd61455d992c123f10d3b01d'))

# Define the Uniswap router contract address and ABI
router_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
router_abi = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountOutMin",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapExactETHForTokens",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    }
]

# Initialize the contract
router_contract = web3.eth.contract(address=router_address, abi=router_abi)


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
    url = f'https://api.coingecko.com/api/v3/coins/ethereum?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false'
    response = requests.get(url)
    address = "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"
    liquidty = get_uniswap_liquidity(address)
    print(liquidty)
    if response.status_code == 200:
        data = response.json()
        token_info = {
            'name': data['name'],
            'symbol': data['symbol'].upper(),
            'market_cap': data['market_data']['market_cap']['usd'],
            'price': data['market_data']['current_price']['usd']
        }
        return token_info
    else:
        print("Error fetching data:", response.status_code)
        return None


def get_uniswap_liquidity(pair_address):
    # GraphQL query to get liquidity data for a specific pair
    query = """
    {
        pair(id: "%s") {
            id
            reserveUSD
            reserveETH
            token0 {
                id
                symbol
                name
            }
            token1 {
                id
                symbol
                name
            }
        }
    }
    """ % pair_address

    url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'

    response = requests.post(url, json={'query': query})
    if response.status_code == 200:
        data = response.json()
        return data['data']['pair']
    else:
        raise Exception(f"Query failed to run with a {
                        response.status_code}. {response.text}")
