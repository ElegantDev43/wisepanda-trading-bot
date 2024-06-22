import requests
import json

def get_metadata(token):
  url = "https://mainnet.helius-rpc.com/?api-key=c05d1904-280f-42c5-affc-a66bd9247093"
  payload = {
    "jsonrpc": "2.0",
    "id": "id",
    "method": "getAsset",
    "params": {
      "id": token
    }
  }

  headers = {
    "Content-Type": "application/json"
  }

  response = requests.post(url, headers=headers, data=json.dumps(payload))
  result = response.json()['result']

  name = result['content']['metadata']['name']
  symbol = result['content']['metadata']['symbol']
  decimals = result['token_info']['decimals']

  return {
    'name': name,
    'symbol': symbol,
    'decimals': int(decimals)
  }

def check_liveness(token):
  url = 'https://quote-api.jup.ag/v6/quote'
  params = {
    'inputMint': 'So11111111111111111111111111111111111111112',
    'outputMint': token,
    'amount': '100000',
    'slippageBps': '50'
  }
  try:
    response = requests.get(url, params=params)
    quoteResponse = response.json()
    if 'errorCode' in quoteResponse:
      return False
    else:
      return True
  except Exception as e:
    print("Error fetching quote:", e)

def get_market_data(token):
  api_url = f"https://gmgn.ai/defi/quotation/v1/tokens/sol/{token}"

  response = requests.get(api_url)

  if response.status_code == 200:
      data = response.json()
      if data['msg'] == "invalid argument: invalid token address":
        return 999
      elif not data['data']['token']:
        return 999
      else:
        token_price = data['data']['token']['price']
        liquidity = data['data']['token']['liquidity']
        market_cap = data['data']['token']['market_cap']
        print(f"Token Price: {token_price:.18f}")
        print(f"Liquidity: {liquidity}")
        print(f"Market Cap: {market_cap}")
        return {'price':token_price, 'liquidity':liquidity, 'market_cap':market_cap}
  else:
      print(f"Failed to fetch data. Status code: {response.status_code}")
      
    
def get_token_price(token):
  url = 'https://quote-api.jup.ag/v6/quote'
  params = {
    'inputMint': 'So11111111111111111111111111111111111111112',
    'outputMint': token,
    'amount': '100000',
    'slippageBps': '50'
  }
  try:
    response = requests.get(url, params=params)
    quoteResponse = response.json()
    return float(quoteResponse['outAmount']) / 100.0
  except Exception as e:
    print("Error fetching quote:", e)