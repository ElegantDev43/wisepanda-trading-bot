from src.engine.wallet import ethereum, solana

def get_wallet_engine(chain):
    if chain == 'ethereum':
        return ethereum
    elif chain == 'solana':
        return solana

def create_wallet(chain):
    wallet_engine = get_wallet_engine(chain)
    return wallet_engine.create_wallet()

def get_address(chain, private_key):
    wallet_engine = get_wallet_engine(chain)
    return wallet_engine.get_address(private_key)

def get_balance(chain, address):
    wallet_engine = get_wallet_engine(chain)
    return wallet_engine.get_balance(address)
