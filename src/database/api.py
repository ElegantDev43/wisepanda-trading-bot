from src.database import user as user_model

def get_users():
  return user_model.gets()

def add_user(user_id):
  user_model.add(user_id)

def get_user(user_id):
  return user_model.get(user_id)

def get_chain(user_id):
  user = get_user(user_id)
  return user.chain

def set_chain(user_id, chain):
  user_model.set(user_id, 'chain', chain)

def get_wallets(user_id, chain):
  user = get_user(user_id)
  return user.wallets[chain]

def add_wallet(user_id, chain, wallet):
  user = get_user(user_id)
  user.wallets[chain].append(wallet)
  user_model.set(user_id, 'wallets', user.wallets)

def get_wallet(user_id, chain, wallet_id):
  user = get_user(user_id)
  for wallet in user.wallets[chain]:
    if wallet['id'] == wallet_id:
      return wallet
  return None

def remove_wallet(user_id, chain, wallet_id):
  user = get_user(user_id)
  for index, wallet in enumerate(user.wallets[chain]):
    if wallet['id'] == wallet_id:
      user.wallets[chain].pop(index)
      break
  user_model.set(user_id, 'wallets', user.wallets)

def get_positions(user_id, chain):
  user = get_user(user_id)
  return list(filter(lambda position: position['chain'] == chain, user.positions))

def add_position(user_id, position):
  user = get_user(user_id)
  user.positions.append(position)
  user_model.set(user_id, 'positions', user.positions)

def get_position(user_id, position_id):
  user = get_user(user_id)
  for position in user.positions:
    if position['id'] == position_id:
      return position
  return None

def set_position(user_id, position_id, position):
  user = get_user(user_id)
  for index in range(len(user.positions)):
    if user.positions[index]['id'] == position_id:
      user.positions[index] = position
      break
  user_model.set(user_id, 'positions', user.positions)

def remove_position(user_id, position_id):
  user = get_user(user_id)
  for index, position in enumerate(user.positions):
    if position['id'] == position_id:
      user.positions.pop(index)
      break
  user_model.set(user_id, 'positions', user.positions)

def get_auto_sniper(user_id, chain):
  user = get_user(user_id)
  return user.auto_sniper[chain]

def set_auto_sniper(user_id, chain, auto_sniper):
  user = get_user(user_id)
  user.auto_sniper[chain] = auto_sniper
  user_model.set(user_id, 'auto_sniper', user.auto_sniper)

def get_token_snipers(user_id, chain):
  user = get_user(user_id)
  return list(filter(lambda token_sniper: token_sniper['chain'] == chain, user.token_snipers))

def add_token_sniper(user_id, token_sniper):
  user = get_user(user_id)
  user.token_snipers.append(token_sniper)
  user_model.set(user_id, 'token_snipers', user.token_snipers)

def get_token_sniper(user_id, token_sniper_id):
  user = get_user(user_id)
  for token_sniper in user.token_snipers:
    if token_sniper['id'] == token_sniper_id:
      return token_sniper
  return None

def set_token_sniper(user_id, token_sniper_id, token_sniper):
  user = get_user(user_id)
  for index in range(len(user.token_snipers)):
    if user.token_snipers[index]['id'] == token_sniper_id:
      user.token_snipers[index] = token_sniper
      break
  user_model.set(user_id, 'token_snipers', user.token_snipers)

def remove_token_sniper(user_id, token_sniper_id):
  user = get_user(user_id)
  for index, token_sniper in enumerate(user.token_snipers):
    if token_sniper['id'] == token_sniper_id:
      user.token_snipers.pop(index)
      break
  user_model.set(user_id, 'token_snipers', user.token_snipers)

def get_lp_snipers(user_id, chain):
  user = get_user(user_id)
  return list(filter(lambda lp_sniper: lp_sniper['chain'] == chain, user.lp_snipers))

def add_lp_sniper(user_id, lp_sniper):
  user = get_user(user_id)
  user.lp_snipers.append(lp_sniper)
  user_model.set(user_id, 'lp_snipers', user.lp_snipers)

def get_lp_sniper(user_id, lp_sniper_id):
  user = get_user(user_id)
  for lp_sniper in user.lp_snipers:
    if lp_sniper['id'] == lp_sniper_id:
      return lp_sniper
  return None

def set_lp_sniper(user_id, lp_sniper_id, lp_sniper):
  user = get_user(user_id)
  for index in range(len(user.lp_snipers)):
    if user.lp_snipers[index]['id'] == lp_sniper_id:
      user.lp_snipers[index] = lp_sniper
      break
  user_model.set(user_id, 'lp_snipers', user.lp_snipers)

def remove_lp_sniper(user_id, lp_sniper_id):
  user = get_user(user_id)
  for index, lp_sniper in enumerate(user.lp_snipers):
    if lp_sniper['id'] == lp_sniper_id:
      user.lp_snipers.pop(index)
      break
  user_model.set(user_id, 'lp_snipers', user.lp_snipers)

def get_limit_orders(user_id, chain):
  user = get_user(user_id)
  return list(filter(lambda limit_order: limit_order['chain'] == chain, user.limit_orders))

def add_limit_order(user_id, limit_order):
  user = get_user(user_id)
  user.limit_orders.append(limit_order)
  user_model.set(user_id, 'limit_orders', user.limit_orders)

def get_limit_order(user_id, limit_order_id):
  user = get_user(user_id)
  for limit_order in user.limit_orders:
    if limit_order['id'] == limit_order_id:
      return limit_order
  return None

def set_limit_order(user_id, limit_order_id, limit_order):
  user = get_user(user_id)
  for index in range(len(user.limit_orders)):
    if user.limit_orders[index]['id'] == limit_order_id:
      user.limit_orders[index] = limit_order
      break
  user_model.set(user_id, 'limit_orders', user.limit_orders)

def remove_limit_order(user_id, limit_order_id):
  user = get_user(user_id)
  for index, limit_order in enumerate(user.limit_orders):
    if limit_order['id'] == limit_order_id:
      user.limit_orders.pop(index)
      break
  user_model.set(user_id, 'limit_orders', user.limit_orders)

def get_dca_orders(user_id, chain):
  user = get_user(user_id)
  return list(filter(lambda dca_order: dca_order['chain'] == chain, user.dca_orders))

def add_dca_order(user_id, dca_order):
  user = get_user(user_id)
  user.dca_orders.append(dca_order)
  user_model.set(user_id, 'dca_orders', user.dca_orders)

def get_dca_order(user_id, dca_order_id):
  user = get_user(user_id)
  for dca_order in user.dca_orders:
    if dca_order['id'] == dca_order_id:
      return dca_order
  return None

def set_dca_order(user_id, dca_order_id, dca_order):
  user = get_user(user_id)
  for index in range(len(user.dca_orders)):
    if user.dca_orders[index]['id'] == dca_order_id:
      user.dca_orders[index] = dca_order
      break
  user_model.set(user_id, 'dca_orders', user.dca_orders)

def remove_dca_order(user_id, dca_order_id):
  user = get_user(user_id)
  for index, dca_order in enumerate(user.dca_orders):
    if dca_order['id'] == dca_order_id:
      user.dca_orders.pop(index)
      break
  user_model.set(user_id, 'dca_orders', user.dca_orders)

def get_auto_order(user_id, chain):
  user = get_user(user_id)
  return user.auto_order[chain]

def set_auto_order(user_id, chain, auto_order):
  user = get_user(user_id)
  user.auto_order[chain] = auto_order
  user_model.set(user_id, 'auto_order', user.auto_order)

def set_user_feature_values(user_id, feature, update_values):
  user = get_user(user_id)
  user.user_feature_values[feature] = update_values
  user_model.set(user_id, 'user_feature_values', user.user_feature_values)

def get_user_feature_values(user_id):
  user = get_user(user_id)
  return user.user_feature_values

def set_auto_swing_status(user_id, value):
  user = get_user(user_id)
  user.auto_swing_status = value
  user_model.set(user_id, 'auto_swing_status', user.auto_swing_status)
  
def get_auto_swing_status(user_id):
  user = get_user(user_id)
  return user.auto_swing_status