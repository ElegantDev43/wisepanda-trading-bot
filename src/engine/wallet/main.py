from src.engine.wallet import ethereum, solana

wallet_engines = {
    'ethereum': ethereum,
    'solana': solana
}

def create_wallet(chain):
    return wallet_engines[chain].create_wallet()

def import_wallet(chain, private_key):
    return wallet_engines[chain].import_wallet(private_key)
