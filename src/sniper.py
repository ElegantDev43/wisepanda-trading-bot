from web3 import Web3
import json
from datetime import datetime
import threading
import time

from src import config
from src import contract

wallet = None
configuration = None

def check_buy():
    symbol = configuration['symbol']

    price = contract.get_price(symbol)
    market_cap = contract.get_price(symbol)
    liquidty = contract.get_liquidity(symbol)
    tax = contract.get_tax(symbol)

    buy = configuration['buy']

    if price > buy['buy_price']:
        return False
    if market_cap < buy['min_market_cap'] or market_cap > buy['max_market_cap']:
        return False
    if liquidty < buy['min_liquidity'] or liquidty > buy['max_liquidity']:
        return False
    if tax > buy['max_buy_tax']:
        return False

    return True

def check_sell():
    symbol = configuration['symbol']

    price = contract.get_price(symbol)
    tax = contract.get_tax(symbol)

    buy = configuration['buy']
    sell = configuration['sell']

    if price < buy['buy_price'] * sell['stop_loss']:
        return buy['buy_quanitity'] * sell['sell_quantity_at_stop_loss']
    if price < buy['buy_price'] * sell['target_price']:
        return 0
    if tax > sell['max_sell_tax']:
        return 0
    return buy['buy_quanitity'] * sell['sell_quantity_at_target']

def update():
    if check_buy():
        gas = {
            'max_gas_price': configuration['max_gas_price'],
            'max_gas_limit': configuration['max_gas_limit'],
            'gas_delta': configuration['buy']['gas_delta']
        }
        contract.order(wallet, configuration['symbol'], 'buy', configuration['buy']['buy_quanitity'], gas)

    sell_quantity = check_sell()
    if sell_quantity > 0:
        gas = {
            'max_gas_price': configuration['max_gas_price'],
            'max_gas_limit': configuration['max_gas_limit'],
            'gas_delta': configuration['sell']['gas_delta']
        }
        contract.order(wallet, configuration['symbol'], 'sell', sell_quantity, gas)

def start(id, flags, paramWallet, paramConfiguration):
    while flags[id]:
        print(f'{id} is running')
        wallet = paramWallet
        configuration = paramConfiguration
        update()
        time.sleep(1)

    print(f'{id} is stopped')