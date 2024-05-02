from web3 import Web3
import requests
import json
import os
from uniswap import Uniswap

import config
from src.database import user as user_model
from src.telegram import main as telegram

def check_token_liveness(token):
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

    try:
        response = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3', json={'query': query})
        data = response.json()
        token_exists = bool(data.get('data', {}).get('pools'))

        return token_exists
    except Exception as e:
        print("Error occurred:", e)
        return False

def get_token_information(token):
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

    try:
        response = requests.post('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3', json={'query': query})
        data = response.json()
        if data.get('data', {}).get('pools'):
            return data.get('data', {}).get('pools', [])[0]
        else:
            return None
    except Exception as e:
        print("Error occurred:", e)
        return False

def trade(user, token, type, amount, wallets):
    from src.engine import main as engine

    user = user_model.get_user_by_id(user)
    chat_id = user.telegram

    wallet = {
        'address': os.getenv('WALLET_ADDRESS'),
        'private_key': os.getenv('WALLET_PRIVATE_KEY')
    }

    uniswap = Uniswap(
        address=wallet['address'],
        private_key=wallet['private_key'],
        version=3,
        provider=config.ETHEREUM_RPC_URL
    )

    eth = '0x0000000000000000000000000000000000000000'

    if type == 'buy':
        tx_hash = uniswap.make_trade(eth, token, amount)
    else:
        tx_hash = uniswap.make_trade(token, eth, amount)

    telegram.bot.send_message(chat_id=chat_id, text=f'Sent transaction: {tx_hash.hex()}')

    user.orders.append({
        'transaction': tx_hash.hex(),
        'chain': 'ethereum',
        'token': token,
        'type': type,
        'amount': amount,
        'wallets': wallets
    })
    user_model.update_user_by_id(user.id, 'orders', user.orders)

    try:
        web3 = Web3(Web3.HTTPProvider(config.ETHEREUM_RPC_URL))
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        status = receipt['status']
        if status == 1:
            telegram.bot.send_message(chat_id=chat_id, text=f'Transaction success: {tx_hash.hex()}')

            user = user_model.get_user_by_id(user.id)

            orders = []
            for order in user.orders:
                if order['transaction'] != tx_hash.hex():
                    orders.append(order)

            positions = user.positions
            position = {
                'chain': 'ethereum',
                'token': token,
                'balance': engine.get_token_balance(user.chain, wallet['address'], token)
            }
            exist = False
            for index in range(len(positions)):
                if positions[index]['chain'] == 'ethereum' and positions[index]['token'] == token:
                    exist = True
                    positions[index] = position
                    break
            if exist is False:
                positions.append(position)

            user_model.update_user_by_id(user.id, 'orders', orders)
            user_model.update_user_by_id(user.id, 'positions', positions)
        elif status == 0:
            print("Transaction failed!")
    except Exception as e:
        print("Error occurred while waiting for transaction confirmation:", e)