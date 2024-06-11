from src.database import user as user_model

def get_user_by_chat_id(chat_id):
  return user_model.get_by_chat_id(chat_id)

def add_user_by_chat_id(chat_id):
  user_model.add_by_chat_id(chat_id)

def get_current_chain_index(chat_id):
  user = user_model.get_by_chat_id(chat_id)
  return user.current_chain_index

def update_current_chain_index(chat_id, chain_index):
  user = user_model.get_by_chat_id(chat_id)
  user_model.update_by_id(user.id, 'current_chain_index', chain_index)

def get_wallets(chat_id, chain_index):
  user = user_model.get_by_chat_id(chat_id)
  return user.wallets[chain_index]

def add_wallet(chat_id, chain_index, wallet):
  user = user_model.get_by_chat_id(chat_id)
  wallets = user.wallets
  wallets[chain_index].append(wallet)
  user_model.update_by_id(user.id, 'wallets', wallets)

def remove_wallet(chat_id, chain_index, wallet_index):
  user = user_model.get_by_chat_id(chat_id)
  wallets = user.wallets
  wallets[chain_index].pop(wallet_index)
  user_model.update_by_id(user.id, 'wallets', wallets)

def get_wallet(chat_id, chain_index, wallet_index):
  user = user_model.get_by_chat_id(chat_id)
  return user.wallets[chain_index][wallet_index]

def update_wallet(chat_id, chain_index, wallet_index, wallet):
  user = user_model.get_by_chat_id(chat_id)
  wallets = user.wallets
  wallets[chain_index][wallet_index] = wallet
  user_model.update_by_id(user.id, 'wallets', wallets)

def get_token_snipers(chat_id, chain_index):
  return