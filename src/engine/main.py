import time
import threading

import config
from src.database import sniper as sniper_model

from src.engine.chain import ethereum
from src.engine.chain import solana

engines = {
    'ethereum': ethereum,
    'solana': solana,
}

auto_sniper_tokens = []

def update():
    while True:
        new_tokens = []
        for token in auto_sniper_tokens:
            if check_token_liveness(token['chain'], token['address']) == True:
                new_tokens.append(token)

        for token in new_tokens:
            users = sniper_model.get_sniper_users_by_token(token['chain'], token['address'])
            for user in users:
                create_order(token['chain'], user['id'], token['address'], 'market', 'buy', user['amount'], user['wallets'])
            sniper_model.remove_sniper_by_token(token['chain'], token['address'])

        time.sleep(config.AUTO_SNIPER_UPDATE_DELAY)

def add_sniper_user(chain, token, user):
    sniper_model.add_sniper_user_by_token(chain, token, user)

    exist = False
    for token in auto_sniper_tokens:
        if token['chain'] == chain and token['address'] == token:
            exist = True
            break
    if not exist:
        auto_sniper_tokens.append({'chain': chain, 'address': token})

def get_hot_tokens(chain):
    return [chain]

def get_token_name(chain, token):
    return engines[chain].get_token_name(token)

def check_token_liveness(chain, token):
    return engines[chain].check_token_liveness(token)

def get_token_exchange_data(chain, token):
    return engines[chain].get_token_exchange_data(token)

def create_order(chain, user, token, type, side, amount, wallets):
    thread = threading.Thread(target=engines[chain].create_order, args=(user, token, type, side, amount, wallets))
    thread.start()

def initialize():
    thread = threading.Thread(target=update)
    thread.start()
