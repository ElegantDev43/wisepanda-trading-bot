def initialize():
    from src.engine import main as engine

    tokens = {
        'usdt': '0xdac17f958d2ee523a2206206994597c13d831ec7',
        'elon': '0x61D8A0d002CED76FEd03E1551c6Dd71dFAC02fD7',
        'usdc': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
    }

    chain = 'ethereum'
    token = tokens['usdc']

    # hot_tokens = engine.get_hot_tokens(chain)
    # print('get_hot_tokens', len(hot_tokens))

    # token_name = engine.get_token_name(chain, token)
    # print('get_token_name', token_name)

    # address, private_key = engine.create_wallet(chain)
    # print('create_wallet', address, private_key)

    # address = engine.import_wallet(chain, private_key)
    # print('import_wallet', address)

    # balance = engine.get_balance(chain, address)
    # print('get_balance', balance)

    # token_balance = engine.get_token_balance(chain, address, token)
    # print('get_token_balance', token_balance)

    token_liveness = engine.check_token_liveness(chain, token)
    print('check_token_liveness', token_liveness)

    token_information = engine.get_token_information(chain, token)
    print('get_token_information', token_information)

    # engine.create_order(chain, 1, token, 'market', 'sell', token_balance / 10**6, [])