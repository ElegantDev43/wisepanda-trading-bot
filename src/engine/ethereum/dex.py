from src.engine.amm import uniswap

def check_token_liveness(token):
    return uniswap.check_token_liveness(token)

def get_token_information(token):
    return uniswap.get_token_information(token)

def trade(user, token, type, amount, wallets):
    uniswap.trade(user, token, type, amount, wallets)