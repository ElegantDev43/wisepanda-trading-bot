from src.database import user as user_model

def initialize():
    user_model.initialize()

def add_user_by_chat_id(chat_id):
    user_model.add_by_chat_id(chat_id)

def get_current_chain_index(chat_id):
    user = user_model.get_by_chat_id(chat_id)
    return user.current_chain_index

def update_current_chain_index(chat_id, index):
    user = user_model.get_by_chat_id(chat_id)
    user_model.update_by_id(user.id, 'current_chain_index', index)

def get_wallets(chat_id):
    user = user_model.get_by_chat_id(chat_id)
    return user.wallets[user.current_chain_index]

def add_wallet(chat_id, address, private_key):
    user = user_model.get_by_chat_id(chat_id)

def remove_wallet(chat_id, chain_index, wallet_index):
    user = user_model.get_by_chat_id(chat_id)

def get_token_snipers(chat_id):
    user = user_model.get_by_chat_id(chat_id)

def add_token_sniper(chat_id, token, amount, criteria):
    user = user_model.get_by_chat_id(chat_id)

def update_token_sniper(chat_id, index, amount, criteria):
    user = user_model.get_by_chat_id(chat_id)

def remove_token_sniper(chat_id, index):
    user = user_model.get_by_chat_id(chat_id)

def get_pending_orders(chat_id):
    user = user_model.get_by_chat_id(chat_id)

def add_pending_order(chat_id, type, tx_hash, token, amount, wallets, criteria):
    user = user_model.get_by_chat_id(chat_id)

def remove_pending_order(chat_id, tx_hash):
    user = user_model.get_by_chat_id(chat_id)

def get_positions(chat_id):
    user = user_model.get_by_chat_id(chat_id)

def add_position(chat_id, token, amount):
    user = user_model.get_by_chat_id(chat_id)

def update_position(chat_id, token, amount):
    user = user_model.get_by_chat_id(chat_id)

def remove_position(chat_id, token):
    user = user_model.get_by_chat_id(chat_id)

def get_limit_orders(chat_id):
    user = user_model.get_by_chat_id(chat_id)

def add_limit_order(chat_id, type, token, amount, criteria):
    user = user_model.get_by_chat_id(chat_id)

def update_limit_order(chat_id, index, type, token, amount, criteria):
    user = user_model.get_by_chat_id(chat_id)

def remove_limit_order(chat_id, index):
    user = user_model.get_by_chat_id(chat_id)

def get_dca_orders(chat_id):
    user = user_model.get_by_chat_id(chat_id)

def add_dca_order(chat_id, type, token, amount, criteria):
    user = user_model.get_by_chat_id(chat_id)

def update_dca_order(chat_id, index, type, token, amount, criteria):
    user = user_model.get_by_chat_id(chat_id)

def remove_dca_order(chat_id, index):
    user = user_model.get_by_chat_id(chat_id)
