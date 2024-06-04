
import secrets
from eth_account import Account
# Generate a new private key


def market_order(type, token, amount, gas, slippage, wallets):
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    address = acct.address
    return address


def limit_order(type, token, amount, limit_token_price, tax, market_cap, liquidity,  wallets):
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    address = acct.address
    return address


def dca_order(type, token, amount, interval, duration, max_dca_price, min_dca_price, wallets):
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    address = acct.address
    return address
