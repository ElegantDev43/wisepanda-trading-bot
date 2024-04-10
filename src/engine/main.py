import threading
import time

import config
import globals
from src.engine.dex import uniswap
from src.database import sniper as sniper_model

def check_token(token):
    return uniswap.check_token(token)

def update():
    while True:
        new_tokens = []
        for token in globals.auto_sniper_tokens:
            if check_token(token):
                new_tokens.append(token)

        for token in new_tokens:
            users = sniper_model.get_users(token)
            for user in users:
                market_order(user)

        time.sleep(config.AUTO_SNIPER_UPDATE_DELAY)

def market_order():
    uniswap.market_order()

def limit_order():
    uniswap.limit_order()

def start():
    thread = threading.Thread(target=update)
    thread.start()
