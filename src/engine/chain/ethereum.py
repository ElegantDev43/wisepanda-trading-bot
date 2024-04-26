from web3 import Web3
import subprocess
import json

import config
from src.engine.amm import uniswap

def get_hot_tokens():
    node_script_path = "./src/engine/chain/hots.js"

    command = ["node", node_script_path]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stdout:
        data = json.loads(stdout.decode("utf-8"))
        data = data[0]['data'][:10]
        return data

    else:
        print("No receiving data.")

    if stderr:
        print("Error:")
        print(stderr.decode("utf-8"))


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
    return uniswap.check_token_liveness(token)

def get_token_information(token):
    return uniswap.get_token_information(token)

def create_order(user, token, type, side, amount, wallets):
    uniswap.create_order(user, token, type, side, amount, wallets)
