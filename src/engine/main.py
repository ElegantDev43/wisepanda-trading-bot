import time
import threading
import os
import http.client
import json
import requests

import config
from src.database import sniper as sniper_model
from src.engine.wallet import main as wallet

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

def add_sniper_user(token, user):
    sniper_model.add_sniper_user_by_token(token, user)
    auto_sniper_tokens.append(token)

def update():
    while True:
        new_tokens = []
        for token in auto_sniper_tokens:
            if check_token_liveness(token) == True:
                new_tokens.append(token)

        for token in new_tokens:
            users = sniper_model.get_sniper_users_by_token(token)
            for user in users:
                create_order(user['id'], token['chain'], token['address'], 'market', 'buy', user['amount'], user['wallets'])
            sniper_model.remove_sniper_by_token(token)

        time.sleep(config.AUTO_SNIPER_UPDATE_DELAY)

def create_order(user, chain, token, type, side, amount, wallets):
    thread = threading.Thread(target=engines[chain].create_order, args=(user, token, type, side, amount, wallets))
    thread.start()

def get_hot_tokens():

    url = 'https://www.dextools.io/shared/hotpairs/hot?chain=ether'
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Referer': 'https://www.dextools.io/app/en/ether/pool-explorer',
        'Referrer-Policy': 'strict-origin-when-cross-origin'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response code is an error code
        data = response.json()
        print(data)
    except requests.exceptions.RequestException as e:
        print('There was a problem with the fetch operation:', e)



def initialize():
    thread = threading.Thread(target=update)
    thread.start()

    get_hot_tokens()