import requests
import json
from solana.rpc.api import Client
from solders.pubkey import Pubkey # type: ignore
from solders.keypair import Keypair # type: ignore
from src.engine.chain.solana.solana_tracker.solanatracker import SolanaTracker
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
    owner = json.loads(account_info).get('owner', '0')
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

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        result = response.json().get('result')

        if not result:
            return 0

        content = result.get('content')
        if not content:
            return 0

        metadata = content.get('metadata')
        if not metadata:
            return 0

        token_info = result.get('token_info')
        if not token_info:
            return 0

        name = metadata.get('name', 0)
        symbol = metadata.get('symbol', 0)
        decimals = token_info.get('decimals', 0)


        return {
            'name': name,
            'symbol': symbol,
            'decimals': int(decimals)
        }
    except requests.RequestException as e:
        print(f"Failed to fetch metadata. Exception: {e}")
        return 0
    except (ValueError, KeyError, TypeError) as e:
        print(f"Error processing the response. Exception: {e}")
        return 0

def check_liveness(token):
  keypair = Keypair()
  solana_tracker = SolanaTracker(keypair, "https://rpc.solanatracker.io/public?advancedTx=true")

  try:
      swap_response = solana_tracker.get_swap_instructions(
          "So11111111111111111111111111111111111111112",  # From Token
          token,  # To Token
          0.0001,  # Amount to swap
          10,  # Slippage
          str(keypair.pubkey()),  # Payer public key
          0.00005,  # Priority fee (Recommended while network is congested)
          True  # Force legacy transaction for Jupiter
      )

      # Check the response for the specific error message
      if swap_response.get('message') == 'To token address is invalid.':
          return False
      else:
          return True

  except Exception as e:
      # Handle exceptions that indicate the swap failed
      return False
  

def get_market_data(token):
    api_url = f"https://gmgn.ai/defi/quotation/v1/tokens/sol/{token}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
        data = response.json()

        if data['msg'] == "invalid argument: invalid token address":
            return 999
        token_data = data.get('data')
        if not token_data:
            return 999
        token_info = token_data.get('token')
        if not token_info:
            return 999

        token_price = token_info.get('price', 0)
        liquidity = token_info.get('liquidity', 0)
        market_cap = token_info.get('market_cap', '1')

        return {'price': token_price, 'liquidity': liquidity, 'market_capital': int(market_cap)}
    except requests.RequestException as e:
        return 0

def get_jupiter_price(token):
  try:
    symbol = get_metadata(token)['symbol']
    response = requests.get(f"https://price.jup.ag/v6/price?ids={symbol}")
    
    if response.status_code == 200:
      resp = response.json()['data']
      if not resp[symbol]:
        return 0
      data = resp[symbol]['price']
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