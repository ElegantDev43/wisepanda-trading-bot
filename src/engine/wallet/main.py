from src.engine.wallet import ethereum, solana

wallets = {
    'ethereum': ethereum,
    'solana': solana
}

def create_wallet(chain):
    return wallets[chain].create_wallet()

def import_wallet(chain, private_key):
    return wallets[chain].import_wallet(private_key)

def get_balance(chain, address):
    return wallets[chain].get_balance(address)

def get_token_balance(chain, address, token):
    return wallets[chain].get_token_balance(address, token)
