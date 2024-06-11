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
    'decimals': decimals
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

def get_information(token):
  price = get_token_price(token)
  return {'price': price}

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