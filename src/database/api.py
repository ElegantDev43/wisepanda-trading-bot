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
  user = user_model.get_by_chat_id(chat_id)
  return user.token_snipers[chain_index]

def add_token_sniper(chat_id, chain_index, token_sniper):
  user = user_model.get_by_chat_id(chat_id)
  token_snipers = user.token_snipers
  token_snipers[chain_index].append(token_sniper)
  user_model.update_by_id(user.id, 'token_snipers', token_snipers)

def remove_token_sniper(chat_id, chain_index, token_sniper_index):
  user = user_model.get_by_chat_id(chat_id)
  token_snipers = user.token_snipers
  token_snipers[chain_index].pop(token_sniper_index)
  user_model.update_by_id(user.id, 'token_snipers', token_snipers)

def get_token_sniper(chat_id, chain_index, timestamp):
  user = user_model.get_by_chat_id(chat_id)
  for token_sniper in user.token_snipers[chain_index]:
    if token_sniper['timestamp'] == timestamp:
      return token_sniper
  return None

def update_token_sniper(chat_id, chain_index, token_sniper_index, token_sniper):
  user = user_model.get_by_chat_id(chat_id)
  token_snipers = user.token_snipers
  token_snipers[chain_index][token_sniper_index] = token_sniper
  user_model.update_by_id(user.id, 'token_snipers', token_snipers)

def get_limit_orders(chat_id, chain_index):
  user = user_model.get_by_chat_id(chat_id)
  return user.limit_orders[chain_index]

def add_limit_order(chat_id, chain_index, limit_order):
  user = user_model.get_by_chat_id(chat_id)
  limit_orders = user.limit_orders
  limit_orders[chain_index].append(limit_order)
  user_model.update_by_id(user.id, 'limit_orders', limit_orders)

def remove_limit_order(chat_id, chain_index, limit_order_index):
  user = user_model.get_by_chat_id(chat_id)
  limit_orders = user.limit_orders
  limit_orders[chain_index].pop(limit_order_index)
  user_model.update_by_id(user.id, 'limit_orders', limit_orders)

def get_limit_order(chat_id, chain_index, timestamp):
  user = user_model.get_by_chat_id(chat_id)
  for limit_order in user.limit_orders[chain_index]:
    if limit_order['timestamp'] == timestamp:
      return limit_order
  return None

def update_limit_order(chat_id, chain_index, limit_order_index, limit_order):
  user = user_model.get_by_chat_id(chat_id)
  limit_orders = user.limit_orders
  limit_orders[chain_index][limit_order_index] = limit_order
  user_model.update_by_id(user.id, 'limit_orders', limit_orders)

def get_dca_orders(chat_id, chain_index):
  user = user_model.get_by_chat_id(chat_id)
  return user.dca_orders[chain_index]

def add_dca_order(chat_id, chain_index, dca_order):
  user = user_model.get_by_chat_id(chat_id)
  dca_orders = user.dca_orders
  dca_orders[chain_index].append(dca_order)
  user_model.update_by_id(user.id, 'dca_orders', dca_orders)

def remove_dca_order(chat_id, chain_index, dca_order_index):
  user = user_model.get_by_chat_id(chat_id)
  dca_orders = user.dca_orders
  dca_orders[chain_index].pop(dca_order_index)
  user_model.update_by_id(user.id, 'dca_orders', dca_orders)

def get_dca_order(chat_id, chain_index, timestamp):
  user = user_model.get_by_chat_id(chat_id)
  for dca_order in user.dca_orders[chain_index]:
    if dca_order['timestamp'] == timestamp:
      return dca_order
  return None

def update_dca_order(chat_id, chain_index, dca_order_index, dca_order):
  user = user_model.get_by_chat_id(chat_id)
  dca_orders = user.dca_orders
  dca_orders[chain_index][dca_order_index] = dca_order
  user_model.update_by_id(user.id, 'dca_orders', dca_orders)