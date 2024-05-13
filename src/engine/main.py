import config

from src.engine import token_sniper

def initialize():
    token_sniper.initialize()

def get_supported_chains():
    return config.CHAINS

def get_current_chain(chat_id):
    return True