from src.database import user as user_model


def add_user_by_chat_id(chat_id):
    user_model.add_by_chat_id(chat_id)


def get_user_by_chat_id(chat_id):
    user = user_model.get_by_chat_id(chat_id)
    return user


def get_keyboards(chat_id):
    user = user_model.get_by_chat_id(chat_id)
    return user.keyboards


def update_keyboards(chat_id, keyboards):
    user = user_model.get_by_chat_id(chat_id)
    user_model.update_by_id(user.id, 'keyboards', keyboards)


def get_supported_chains():
    return [
        'ethereum',
        'solana',
        'base'
    ]


def get_current_chain_index(chat_id):
    user = user_model.get_by_chat_id(chat_id)
    return user.current_chain_index


def update_current_chain_index(chat_id, index):
    user = user_model.get_by_chat_id(chat_id)
    user_model.update_by_id(user.id, 'current_chain_index', index)


def get_wallets(chat_id):
    user = user_model.get_by_chat_id(chat_id)
    chains = get_supported_chains()
    return user.wallets[chains[user.current_chain_index]]


def add_wallet(chat_id, chain_index, address, private_key):
    user = user_model.get_by_chat_id(chat_id)
    chains = get_supported_chains()
    user.wallets[chains[chain_index]].append(
        {"address": address, "privat_key": private_key, "balance": 0, "active": True})
    user_model.update_by_id(user.id, 'wallets', user.wallets)


def import_wallet(chat_id, chain_index, address, private_key, balance):
    user = user_model.get_by_chat_id(chat_id)
    chains = get_supported_chains()
    user.wallets[chains[chain_index]].append(
        {"address": address, "privat_key": private_key, "balance": balance, "active": True})
    user_model.update_by_id(user.id, 'wallets', user.wallets)


def remove_wallet(chat_id, chain_index, wallet_index):
    user = user_model.get_by_chat_id(chat_id)
    chains = get_supported_chains()
    wallet = user.wallets[chains[chain_index]].pop(wallet_index)
    user_model.update_by_id(user.id, 'wallets', user.wallets)


def add_token_sniper(chat_id, tx_hash, token, amount, gas, slippage, wallets, criteria):
    user = user_model.get_by_chat_id(chat_id)
    length = len(user.token_snipers)
    length += 1
    user.token_snipers.append({'id': length, 'tx_hash': tx_hash,
                              'token': token, 'buy_amount': amount,
                               'gas': gas, 'slippage': slippage,
                               'limit_token_price': criteria['limit_token_price'],
                               'market_cap': criteria['market_cap'],
                               'liquidity': criteria['liquidity'],
                               'tax': criteria['tax'], 'wallet': wallets})
    user_model.update_by_id(user.id, 'token_snipers', user.token_snipers)


def get_token_sniper(chat_id, chain_index, token):
    user = user_model.get_by_chat_id(chat_id)


def get_token_snipers(chat_id):
    user = user_model.get_by_chat_id(chat_id)
    return user.token_snipers


def update_token_sniper(chat_id, tx_hash, token, amount, gas, slippage, criteria):
    user = user_model.get_by_chat_id(chat_id)
    update_index = 0
    for index in range(len(user.token_snipers)):
        if user.token_snipers[index]['tx_hash'] == tx_hash:
            update_index = index
    user.token_snipers[update_index]['token'] = token
    user.token_snipers[update_index]['buy_amount'] = amount
    user.token_snipers[update_index]['gas'] = gas
    user.token_snipers[update_index]['slippage'] = slippage
    user.token_snipers[update_index]['limit_token_price'] = criteria['limit_token_price']
    user.token_snipers[update_index]['market_cap'] = criteria['market_cap']
    user.token_snipers[update_index]['tax'] = criteria['tax']
    user.token_snipers[update_index]['liquidity'] = criteria['liquidity']
    user_model.update_by_id(user.id, 'token_snipers', user.token_snipers)


def remove_token_sniper(chat_id, tx_hash):
    user = user_model.get_by_chat_id(chat_id)
    removal_index = 0
    for index in range(len(user.dca_orders)):
        if user.token_snipers[index]['tx_hash'] == tx_hash:
            removal_index = index
    orders = user.token_snipers.pop(removal_index)
    user_model.update_by_id(user.id, 'token_snipers', user.token_snipers)


def get_pending_orders(chat_id):
    user = user_model.get_by_chat_id(chat_id)
    return user.pending_orders


def add_pending_order(chat_id, type, tx_hash, token, amount, wallets, criteria):
    user = user_model.get_by_chat_id(chat_id)
    length = len(user.pending_orders)
    length += 1
    user.pending_orders.append({'id': length, 'type': type, 'tx_hash': tx_hash,
                                'token': token, 'buy_amount': amount, 'gas_amount': criteria['gas_amount'], 'gas_price': criteria['gas_price'], 'slippage': criteria['slippage'], 'wallet': wallets})
    user_model.update_by_id(user.id, 'pending_orders', user.pending_orders)


def remove_pending_order(chat_id, tx_hash):
    user = user_model.get_by_chat_id(chat_id)
    removal_index = 0
    for index in range(len(user.pending_orders)):
        if user.pending_orders[index]['tx_hash'] == tx_hash:
            removal_index = index
    orders = user.pending_orders.pop(removal_index)
    user_model.update_by_id(user.id, 'pending_orders', user.pending_orders)


def get_positions(chat_id):
    user = user_model.get_by_chat_id(chat_id)


def add_position(chat_id, token, amount):
    user = user_model.get_by_chat_id(chat_id)


def update_position(chat_id, token, amount):
    user = user_model.get_by_chat_id(chat_id)


def remove_position(chat_id, token):
    user = user_model.get_by_chat_id(chat_id)


def add_limit_order(chat_id, thread_id, type, tx_hash, token, amount, wallets, criteria):
    user = user_model.get_by_chat_id(chat_id)
    length = len(user.limit_orders)
    length += 1
    user.limit_orders.append({'id': length, 'thread_id': thread_id, 'type': type, 'tx_hash': tx_hash,
                              'token': token, 'buy_amount': amount,
                              'limit_token_price': criteria['limit_token_price'],
                              'stop-loss': criteria['stop-loss'],
                              'market_cap': criteria['market_cap'],
                              'liquidity': criteria['liquidity'],
                              'tax': criteria['tax'], 'wallet': wallets})
    user_model.update_by_id(user.id, 'limit_orders', user.limit_orders)


def get_limit_orders(chat_id):
    user = user_model.get_by_chat_id(chat_id)
    return user.limit_orders


def update_limit_order(chat_id, type, tx_hash, token, amount, criteria):
    user = user_model.get_by_chat_id(chat_id)
    update_index = 0
    for index in range(len(user.limit_orders)):
        if user.limit_orders[index]['tx_hash'] == tx_hash:
            update_index = index
    user.limit_orders[update_index]['type'] = type
    user.limit_orders[update_index]['token'] = token
    user.limit_orders[update_index]['buy_amount'] = amount
    user.limit_orders[update_index]['limit_token_price'] = criteria['limit_token_price']
    user.limit_orders[update_index]['stop-loss'] = criteria['stop-loss']
    user.limit_orders[update_index]['market_cap'] = criteria['market_cap']
    user.limit_orders[update_index]['tax'] = criteria['tax']
    user.limit_orders[update_index]['liquidity'] = criteria['liquidity']
    user_model.update_by_id(user.id, 'limit_orders', user.limit_orders)


def remove_limit_order(chat_id, tx_hash):
    user = user_model.get_by_chat_id(chat_id)
    removal_index = 0
    for index in range(len(user.limit_orders)):
        if user.limit_orders[index]['thread_id'] == tx_hash:
            removal_index = index
    orders = user.limit_orders.pop(removal_index)
    user_model.update_by_id(user.id, 'limit_orders', user.limit_orders)


def get_dca_orders(chat_id):
    user = user_model.get_by_chat_id(chat_id)
    return user.dca_orders


def add_dca_order(chat_id, thread_id, type, tx_hash, token, amount, wallets, criteria):
    user = user_model.get_by_chat_id(chat_id)
    length = len(user.dca_orders)
    length += 1
    user.dca_orders.append({'id': length, 'thread_id': thread_id, 'type': type, 'tx_hash': tx_hash,
                            'token': token, 'buy_amount': amount,
                            'interval': criteria['interval'],
                            'duration': criteria['duration'],
                            'max_dca_price': criteria['max_dca_price'],
                            'min_dca_price': criteria['min_dca_price'], 'wallet': wallets})
    user_model.update_by_id(user.id, 'dca_orders', user.dca_orders)


def update_dca_order(chat_id, type, tx_hash, token, amount, criteria):
    user = user_model.get_by_chat_id(chat_id)
    update_index = 0
    for index in range(len(user.dca_orders)):
        if user.dca_orders[index]['tx_hash'] == tx_hash:
            update_index = index
    user.dca_orders[update_index]['type'] = type
    user.dca_orders[update_index]['token'] = token
    user.dca_orders[update_index]['buy_amount'] = amount
    user.dca_orders[update_index]['interval'] = criteria['interval']
    user.dca_orders[update_index]['duration'] = criteria['duration']
    user.dca_orders[update_index]['min_dca_price'] = criteria['min_dca_price']
    user.dca_orders[update_index]['max_dca_price'] = criteria['max_dca_price']
    user_model.update_by_id(user.id, 'dca_orders', user.dca_orders)


def remove_dca_order(chat_id, tx_hash):
    user = user_model.get_by_chat_id(chat_id)
    removal_index = 0
    for index in range(len(user.dca_orders)):
        if user.dca_orders[index]['thread_id'] == tx_hash:
            removal_index = index
    orders = user.dca_orders.pop(removal_index)
    user_model.update_by_id(user.id, 'dca_orders', user.dca_orders)
