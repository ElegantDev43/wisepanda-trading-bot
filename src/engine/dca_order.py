import time

from src.database import api as database
from src.engine.chain import token as token_engine
from src.engine.chain import dex as dex_engine
from src.engine import criteria as criteria_engine

def start(chat_id, chain_index, token):
    while True:
        data = database.get_limit_orders(chat_id, chain_index, token)

        if data:
            if token_engine.check_liveness(chain_index, token):
                amount, gas, slippage, wallets, criteria = data
                max_price, min_liquidity, max_market_captial, max_buy_tax = criteria
                
                if criteria_engine.check(chain_index, token, (None, max_price, min_liquidity, max_market_captial, max_buy_tax, None)):
                    dex_engine.market_order(chain_index, 'buy', token, amount, gas, slippage, wallets)
                    database.remove_token_sniper(chat_id, chain_index, token)

                break
        else:
            break

        time.sleep(10)