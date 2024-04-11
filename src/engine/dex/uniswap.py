from web3 import Web3
import requests
from web3.middleware import geth_poa_middleware
import json
import threading
import time
import os

import config

def check_token(token_address):
    query = """
    {
        tokens(where: {id: "%s"}) {
            id
            symbol
        }
    }
    """ % token_address.lower()

    try:
        response = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2', json={'query': query})
        data = response.json()
        if data.get('data', {}).get('tokens'):
            return True
        else:
            return False
    except Exception as e:
        print("Error occurred:", e)
        return False

def create_order(wallet, token, type, amount):
    web3 = Web3(Web3.HTTPProvider(config.ETHEREUM_RPC_URL))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    with open('./src/engine/dex/uniswap_router_abi.json', 'r') as f:
        uniswap_router_abi = json.load(f)
    uniswap_router_address = '0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD'
    router_contract = web3.eth.contract(address=uniswap_router_address, abi=uniswap_router_abi)

    if type == 'buy':
        commands = bytes.fromhex('0b00')
        input1 = bytes.fromhex('000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000038D7EA4C68000')
        input2 = bytes.fromhex('000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000038D7EA4C68000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002bfff9976782d46cc05630d1f6ebab18b2324d6b14002710' + token[2:] + '000000000000000000000000000000000000000000')
        inputs = [input1, input2]

        gas_price = web3.eth.gas_price
        amount_eth = int(web3.to_wei(amount, 'ether'))

        tx = router_contract.functions.execute(
            commands,
            inputs,
            int(time.time()) + 1000
        ).build_transaction({
            'from': wallet['address'],
            'gas': 2000000,
            'gasPrice': gas_price,
            'nonce': web3.eth.get_transaction_count(wallet['address']),
            'value': amount_eth,
        })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=wallet['private_key'])

    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f'Transaction sent: {tx_hash.hex()}')

wallet = {
    'address': os.getenv('WALLET_ADDRESS'),
    'private_key': os.getenv('WALLET_PRIVATE_KEY')
}
token = '0x7169D38820dfd117C3FA1f22a697dBA58d90BA06'
type = 'buy'
amount = 0.01
create_order(wallet, token, type, amount)

# thread = threading.Thread(target=create_order)
# thread.start()