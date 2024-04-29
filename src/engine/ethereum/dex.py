from src.engine.amm import uniswap

def check_token_liveness(token):
    return uniswap.check_token_liveness(token)

def get_token_information(token):
    return uniswap.get_token_information(token)

def create_order(user, token, type, side, amount, wallets):
    uniswap.create_order(user, token, type, side, amount, wallets)