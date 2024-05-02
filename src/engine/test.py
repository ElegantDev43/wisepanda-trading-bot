import os
from uniswap import Uniswap
from web3 import Web3

import config

def initialize():
    from src.engine import main as engine

    tokens = {
        'usdt': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
        'elon': '0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7',
        'usdc': '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
        'weth': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        'eth': '0x0000000000000000000000000000000000000000',
    }

    chain = 'ethereum'
    token = tokens['usdc']

    wallet = {
        'address': os.getenv('WALLET_ADDRESS'),
        'private_key': os.getenv('WALLET_PRIVATE_KEY')
    }

    # uniswap = Uniswap(
    #     address=wallet['address'],
    #     private_key=wallet['private_key'],
    #     version=3,
    #     provider=config.ETHEREUM_RPC_URL
    # )

    # price = uniswap.get_price_input(tokens['eth'], tokens['usdt'], 10**18)
    # print('price', price)

    # tx_hash = uniswap.make_trade(tokens['usdc'], tokens['eth'], 10**6)
    # print('tx_hash', tx_hash.hex())

    # hot_tokens = engine.get_hot_tokens(chain)
    # print('get_hot_tokens', len(hot_tokens))

    # token_name = engine.get_token_name(chain, token)
    # print('get_token_name', token_name)

    # address, private_key = engine.create_wallet(chain)
    # print('create_wallet', address, private_key)

    # address = engine.import_wallet(chain, private_key)
    # print('import_wallet', address)

    # balance = engine.get_balance(chain, address)
    # print('get_balance', balance)

    # token_balance = engine.get_token_balance(chain, wallet['address'], token)
    # print('get_token_balance', token_balance)

    # token_liveness = engine.check_token_liveness(chain, token)
    # print('check_token_liveness', token_liveness)

    # token_information = engine.get_token_information(chain, token)
    # print('get_token_information', token_information)

    # engine.trade(chain, 1, token, 'market', 'sell', token_balance / 10**6, [])