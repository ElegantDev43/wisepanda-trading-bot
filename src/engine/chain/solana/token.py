import requests

def get_name(token):
  return 'Token Name'

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