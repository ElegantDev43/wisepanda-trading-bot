import requests
import json
from solana.rpc.api import Client
from solders.pubkey import Pubkey # type: ignore
import base58
import re

def is_valid(token):
  pattern = re.compile(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$')
  if not pattern.match(token):
    return False

  try:
    decoded_token = base58.b58decode(token)
    if len(decoded_token) != 32:
      return False
  except ValueError:
    return False

  client = Client("https://api.mainnet-beta.solana.com")

  try:
    account_info = client.get_account_info(Pubkey.from_string(token)).value.to_json()
    owner = json.loads(account_info)['owner']
    token_program_id = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
    if str(owner) == token_program_id:
      return True
    else:
      return False
  except Exception:
    return False

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
  if get_jupiter_price(token) > 0:
    return 'jupiter'
  elif get_raydium_price(token) > 0:
    return 'raydium'
  
  PUMPFUN_METADATA_API = "https://pumpportal.fun/api/data/token-info?ca="
  response = requests.get(PUMPFUN_METADATA_API + token)
  if response.status_code == 200:
    data = response.json()
    if data.get('data'):
      return 'pumpfun'
    else:
      return False

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
      return {'price':token_price, 'liquidity':liquidity, 'market_capital':market_cap}
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

def get_jupiter_price(token):
  try:
    symbol = get_metadata(token)
    response = requests.get(f"https://price.jup.ag/v6/price?ids={symbol}")
    
    if response.status_code == 200:
      data = response.json()['data'][symbol]['price']
      return data
    else:
      return 0
  except requests.exceptions.RequestException:
    return 0
  except (ValueError, KeyError):
    return 0
    
def get_raydium_price(token):
  query = """
  subscription {
  Solana {
    DEXTradeByTokens(
    where: {Trade: {Currency: {MintAddress: {is: "%s"}}, Side: {Currency: {MintAddress: {is: "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"}}}}}
    ) {
    Trade {
      Price
    }
    }
  }
  }
  """ % token
  
  headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
  }
  
  try:
    RAYDIUM_GRAPHQL_ENDPOINT = "https://streaming.bitquery.io/eap?token=ory_at_iVWFAk0YQWWrLfZ6B3-klhgXDeLpKHrCdmsvJSrUnwo.YUTDgW22bhZHCp7p86Eu3aMTu_x4ntOE2ZUAzpxZpWc"
    response = requests.post(RAYDIUM_GRAPHQL_ENDPOINT, json={'query': query}, headers=headers)
    if response.status_code == 200:
      data = response.json()
      price = data['data']['Solana']['DEXTradeByTokens'][0]['Trade']['Price']
      return price
    else:
      raise 0
  except Exception as e:
    return 0