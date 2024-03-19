from web3 import Web3
import json
from datetime import datetime

web3 = Web3(Web3.HTTPProvider('https://eth-sepolia.g.alchemy.com/v2/demo'))

with open('contract_abi.json', 'r') as f:
    contract_abi = json.load(f)

contract_address = Web3.to_checksum_address('0xd0730b305b520cece4e5fa779e6f2dcf297b453e')

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

wallet_address = '0xa69876a83E11f778B2c7492f02b606bf2BBe52a8'
private_key = '08b17887d76a90941c0ab920b585a4c7a578235138a8d3e483e494e17cbabc19'

nonce = web3.eth.get_transaction_count(wallet_address)
params = {
    'market': wallet_address,
    'deadline': int(datetime(year=2024, month=4, day=1).timestamp()),
    'user': wallet_address,
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

signed_txn = web3.eth.account.sign_transaction(txn_dict, private_key)

# tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
# print("Transaction sent. Hash:", tx_hash.hex())

# receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
# print("Transaction mined. Gas used:", receipt.gasUsed)