import time
import threading

import config
from src.database import sniper as sniper_model

auto_sniper_tokens = []

def update():
    from src.engine import main as engine
    
    while True:
        new_tokens = []
        for token in auto_sniper_tokens:
            if engine.check_token_liveness(token['chain'], token['address']) == True:
                new_tokens.append(token)

        for token in new_tokens:
            users = sniper_model.get_sniper_users_by_token(token['chain'], token['address'])
            for user in users:
                engine.create_order(token['chain'], user['id'], token['address'], 'market', 'buy', user['amount'], user['wallets'])
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

def initialize():
    thread = threading.Thread(target=update)
    thread.start()
