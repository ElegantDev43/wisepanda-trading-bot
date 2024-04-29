def initialize():
    from src.engine import main as engine

    chain = 'ethereum'
    token = '0x7169D38820dfd117C3FA1f22a697dBA58d90BA06'

    hot_tokens = engine.get_hot_tokens(chain)
    print('get_hot_tokens', len(hot_tokens))

    token_name = engine.get_token_name(chain, token)
    print('get_token_name', token_name)

    address, private_key = engine.create_wallet(chain)
    print('create_wallet', address, private_key)

    address = engine.import_wallet(chain, private_key)
    print('import_wallet', address)

    balance = engine.get_balance(chain, address)
    print('get_balance', balance)

    token_balance = engine.get_token_balance(chain, address, token)
    print('get_token_balance', token_balance)

    token_liveness = engine.check_token_liveness(chain, token)
    print('check_token_liveness', token_liveness)

    token_information = engine.get_token_information(chain, token)
    print('get_token_information', token_information)

    engine.create_order(chain, 1, token, 'market', 'buy', 0.01, [])