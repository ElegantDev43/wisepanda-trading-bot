from src.engine.chain import token as token_engine

def check(chain, token, criteria):
  min_price, max_price, min_liquidity, min_market_capital = (criteria['min_price'], criteria['max_price'], criteria['min_liquidity'], criteria['min_market_capital'])
  price, liquidity, market_capital = token_engine.get_market_data(chain, token)

  if min_price and price < min_price:
    return False
  if max_price and price > max_price:
    return False
  if min_liquidity and liquidity < min_liquidity:
    return False
  if min_market_capital and market_capital < min_market_capital:
    return False
  
  return True