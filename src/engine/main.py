import threading
import time
import requests
import threading

import config
from src.database import sniper as sniper_model

from src.engine.dex.uniswap import main as ethereum
from src.engine.solana import main as solana

engines = {
    'ethereum': ethereum,
    'solana': solana
}

auto_sniper_tokens = []

def get_token_name(token):
    return engines[token['chain']].get_token_name(token['address'])

def check_token_liveness(token):
    return engines[token['chain']].check_token_liveness(token['address'])

def get_token_exchange_data(token):
    return engines[token['chain']].get_token_exchange_data(token['address'])

def update():
    while True:
        new_tokens = []
        for token in auto_sniper_tokens:
            if check_token_liveness(token) == True:
                new_tokens.append(token)

        for token in new_tokens:
            users = sniper_model.get_users_by_token(token['address'])
            for user in users:
                create_order(token['chain'], token['address'], 'market', 'buy', user['amount'], user['wallets'])
            sniper_model.remove_token(token['address'])

        time.sleep(config.AUTO_SNIPER_UPDATE_DELAY)

def create_order(chain, token, type, side, amount, wallets):
    engines[chain].create_order(token, type, side, amount, wallets)

def initialize():
    thread = threading.Thread(target=update)
    thread.start()

    # token_name = get_token_name({
    #     'chain': 'ethereum',
    #     'address': '0x7169D38820dfd117C3FA1f22a697dBA58d90BA06'
    # })
    # print('token_name', token_name)
