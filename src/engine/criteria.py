from src.engine.chain import token as token_engine

def check(chain_index, token, criteria):
    min_price, max_price, min_liquidity, max_market_capital, max_buy_tax, max_sell_tax = criteria
    price, liquidity, market_capital, buy_tax, sell_tax = token_engine.get_information(chain_index, token)

    if min_price and price < min_price:
        return False
    if max_price and price > max_price:
        return False
    if min_liquidity and liquidity < min_liquidity:
        return False
    if max_market_capital and market_capital > max_market_capital:
        return False
    if max_buy_tax and buy_tax > max_buy_tax:
        return False
    if max_sell_tax and sell_tax > max_sell_tax:
        return False
    
    return True