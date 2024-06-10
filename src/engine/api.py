import config

from src.database.api import main as database

from src.engine import token_sniper as token_sniper_engine
from src.engine import limit_order as limit_order_engine
from src.engine import dca_order as dca_order_engine

from src.engine.chain import wallet as wallet_engine
from src.engine.chain import token as token_engine
from src.engine.chain import amm as amm_engine
from src.engine.chain import hot as hot_engine

def get_supported_chains():
    return config.CHAINS

def get_current_chain_index(chat_id):
    return database.get_current_chain_index(chat_id)

def update_current_chain_index(chat_id, index):
    database.update_current_chain_index(chat_id, index)

def get_wallets(chat_id):
    return database.get_wallets(chat_id)

def create_wallet(chat_id):
    chain_index = get_current_chain_index(chat_id)
    address, private_key = wallet_engine.create_wallet(chain_index)
    database.add_wallet(chat_id, chain_index, address, private_key)
    return address, private_key

def import_wallet(chat_id, private_key):
    chain_index = get_current_chain_index(chat_id)
    address = wallet_engine.import_wallet(chain_index, private_key)
    database.add_wallet(chat_id, chain_index, address, private_key)
    return address

def remove_wallet(chat_id, wallet_index):
    chain_index = get_current_chain_index(chat_id)
    database.remove_wallet(chat_id, chain_index, wallet_index)