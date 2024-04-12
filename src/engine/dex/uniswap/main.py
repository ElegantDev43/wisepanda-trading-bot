from web3 import Web3
import requests
from web3.middleware import geth_poa_middleware
import json
import time

import config

def get_token_name(token):
    web3 = Web3(Web3.HTTPProvider(config.ETHEREUM_RPC_URL))
    token_address = token
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

def check_token_liveness(token):
    return get_token_exchange_data(token) != None

def get_token_exchange_data(token):
    query = """
    {
        tokens(where: {id: "%s"}) {
            id
            name
            symbol
            derivedETH
            totalLiquidity
        }
    }
    """ % token.lower()

    try:
        response = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2', json={'query': query})
        data = response.json()
        if data.get('data', {}).get('tokens'):
            return data.get('data', {}).get('tokens', [])[0]
        else:
            return None
    except Exception as e:
        print("Error occurred:", e)
        return False

def create_order(token, type, side, amount, wallets):
    web3 = Web3(Web3.HTTPProvider(config.ETHEREUM_RPC_URL))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    with open('./src/engine/dex/uniswap/abi.json', 'r') as f:
        uniswap_router_abi = json.load(f)
    uniswap_router_address = '0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD'
    router_contract = web3.eth.contract(address=uniswap_router_address, abi=uniswap_router_abi)

    wallet = wallets[0]

    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(wallet['address'])

    if side == 'buy':
        amount_eth = int(web3.to_wei(amount, 'ether'))
        amount_hex = hex(amount_eth)[2:].zfill(64)

        commands = bytes.fromhex('0b00')
        input1 = bytes.fromhex(f'0000000000000000000000000000000000000000000000000000000000000002{amount_hex}')
        input2 = bytes.fromhex(f'0000000000000000000000000000000000000000000000000000000000000001{amount_hex}000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002bfff9976782d46cc05630d1f6ebab18b2324d6b14002710{token[2:]}000000000000000000000000000000000000000000')
        inputs = [input1, input2]

        tx = router_contract.functions.execute(
            commands,
            inputs,
            int(time.time()) + 1000
        ).build_transaction({
            'from': wallet['address'],
            'value': amount_eth,
            'gas': 1000000,
            'gasPrice': gas_price,
            'nonce': nonce,
        })
    else:
        amount_usd = int(amount * 10**6)
        amount_hex = hex(amount_usd)[2:].zfill(64)

        commands = bytes.fromhex('000c')
        input1 = bytes.fromhex(f'0000000000000000000000000000000000000000000000000000000000000002{amount_hex}000000000000000000000000000000000000000000000000000c1e1cceec764500000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002b{token[2:]}002710fff9976782d46cc05630d1f6ebab18b2324d6b14000000000000000000000000000000000000000000')
        input2 = bytes.fromhex(f'0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000c1e1cceec7645')
        inputs = [input1, input2]

        tx = router_contract.functions.execute(
            commands,
            inputs,
            int(time.time()) + 1000
        ).build_transaction({
            'from': wallet['address'],
            'gas': 1000000,
            'gasPrice': gas_price,
            'nonce': nonce,
        })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=wallet['private_key'])

    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f'Transaction sent: {tx_hash.hex()}')

    try:
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        status = receipt['status']
        if status == 1:
            print("Transaction successful!")
        elif status == 0:
            print("Transaction failed!")
    except Exception as e:
        print("Error occurred while waiting for transaction confirmation:", e)
