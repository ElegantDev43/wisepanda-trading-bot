import threading

from src.engine import sniper, test

from src.engine.ethereum import main as ethereum
from src.engine.solana import main as solana

engines = {
    'ethereum': ethereum,
    'solana': solana,
}

def add_sniper_user(chain, token, user):
    sniper.add_sniper_user(chain, token, user)

def get_hot_tokens(chain):
    return engines[chain].get_hot_tokens()

def get_token_name(chain, token):
    return engines[chain].get_token_name(token)

def create_wallet(chain):
    return engines[chain].create_wallet()

def import_wallet(chain, private_key):
    return engines[chain].import_wallet(private_key)

def get_balance(chain, address):
    return engines[chain].get_balance(address)

def get_token_balance(chain, address, token):
    return engines[chain].get_token_balance(address, token)

def check_token_liveness(chain, token):
    return engines[chain].check_token_liveness(token)

def get_token_information(chain, token):
    return engines[chain].get_token_information(token)

def trade(chain, user, token, type, amount, wallets):
    thread = threading.Thread(target=engines[chain].trade, args=(user, token, type, amount, wallets))
    thread.start()

def initialize():
    sniper.initialize()
    test.initialize()