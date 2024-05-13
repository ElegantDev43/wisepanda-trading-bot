import config

from src.database import main as database
from src.engine import token_sniper

def initialize():
    token_sniper.initialize()

def get_supported_chains():
    return config.CHAINS

def get_current_chain_index(chat_id):
    return database.get_current_chain_index(chat_id)

def update_current_chain_index(chat_id, index):
    database.update_current_chain_index(chat_id, index)