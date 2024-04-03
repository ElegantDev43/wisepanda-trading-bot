from web3 import Web3
import json
from datetime import datetime
import threading
import time

import src.config as config

def get_price(symbol):
    return 0

def get_maret_cap(symbol):
    return 0

def get_liquidity(symbol):
    return 0

def get_tax(symbol):
    return 0

def order(wallet, symbol, side, quantity, gas):
    web3 = Web3(Web3.HTTPProvider('https://eth-sepolia.g.alchemy.com/v2/demo'))

    with open('abi.json', 'r') as f:
        contract_abi = json.load(f)
    contract_address = Web3.to_checksum_address('0xd0730b305b520cece4e5fa779e6f2dcf297b453e')
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    nonce = web3.eth.get_transaction_count(config.WALLET_ADDRESS)
    params = {
        'market': config.WALLET_ADDRESS,
        'deadline': int(datetime(year=2024, month=4, day=1).timestamp()),
        'user': config.WALLET_ADDRESS,
        'limitPriceIndex': 1,
        'rawAmount': 100,
        'expendInput': False,
        'useNative': True,
        'baseAmount': 10
    }
    txn_dict = contract.functions.marketBid(params).build_transaction({
        'chainId': 11155111,
        'gas': 1000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = web3.eth.account.sign_transaction(txn_dict, config.PRIVATE_KEY)

    try:
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print("Transaction sent. Hash:", tx_hash.hex())

        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print("Transaction mined. Gas used:", receipt.gasUsed)
    except Exception as e:
        print('Error:', e)