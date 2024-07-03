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
  
  
def get_from_gmgn(token):
    api_url = f"https://gmgn.ai/defi/quotation/v1/tokens/sol/{token}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
        data = response.json()

        if data['msg'] == "invalid argument: invalid token address":
            return None
        token_data = data.get('data')
        if not token_data:
            return None
        token_info = token_data.get('token')
        if not token_info:
            return None

        Volume = {
            'm5': token_info['volume_5m'],
            'h1': token_info['volume_1h'],
            'h6': token_info['volume_6h'],
            'h24': token_info['volume_24h'],
        }
        Transaction = {
            'm5': token_info['swaps_5m'],
            'h1': token_info['swaps_1h'],
            'h6': token_info['swaps_6h'],
            'h24': token_info['swaps_24h'],
        }
        price = token_info['price']
        liquidity = token_info['liquidity']
        if 'market_cap' in token_info:
          market_cap = token_info['market_cap']
        else:
          market_cap = 0
        return {'tx_count':Transaction, 'volume':Volume, 'price': price, 'liquidity':liquidity, 'market_capital':market_cap}
    except requests.RequestException as e:
        return None

sol_token = 'So11111111111111111111111111111111111111112'
def get_from_dexscreener(token):
    url = f'https://api.dexscreener.com/latest/dex/search?q=So11111111111111111111111111111111111111112%20{token}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def dex_screener_filter(token, response):
  token_pairs = response['pairs']

  reliable_pairs = []
  for pair in token_pairs:
    if (pair['baseToken']['address'] == token and pair['quoteToken']['address'] == sol_token) or (pair['baseToken']['address'] == sol_token and pair['quoteToken']['address'] == token):
      reliable_pairs.append(pair)
  return reliable_pairs

def get_token_info(reliable_pairs):
    m5_transactions = 0
    h1_transactions = 0
    h6_transactions = 0
    h24_transactions = 0

    m5_volume = 0
    h1_volume = 0
    h6_volume = 0
    h24_volume = 0

    m5_priceChange = 0
    h1_priceChange = 0
    h6_priceChange = 0
    h24_priceChange = 0

    liquidity = 0
    fdv = 0
    fdv_count = 0
    length = len(reliable_pairs)

    price = 0
    for pair in reliable_pairs:
        m5_transactions += (pair['txns']['m5']['buys'] + pair['txns']['m5']['sells'])
        h1_transactions += (pair['txns']['h1']['buys'] + pair['txns']['h1']['sells'])
        h6_transactions += (pair['txns']['h6']['buys'] + pair['txns']['h6']['sells'])
        h24_transactions += (pair['txns']['h24']['buys'] + pair['txns']['h24']['sells'])

        m5_volume += pair['volume']['m5']
        h1_volume += pair['volume']['h1']
        h6_volume += pair['volume']['h6']
        h24_volume += pair['volume']['h24']

        m5_priceChange += pair['priceChange']['m5']
        h1_priceChange += pair['priceChange']['h1']
        h6_priceChange += pair['priceChange']['h6']
        h24_priceChange += pair['priceChange']['h24']

        liquidity += pair['liquidity']['usd']
        price += float(pair['priceUsd'])
        if 'fdv' in pair:
            fdv += pair['fdv']
            fdv_count += 1

    Transaction = {
        'm5': m5_transactions,
        'h1': h1_transactions,
        'h6': h6_transactions,
        'h24': h24_transactions
    }
    Volume = {
        'm5': m5_volume / length,
        'h1': h1_volume / length,
        'h6': h6_volume / length,
        'h24': h24_volume / length
    }
    priceChange = {
        'm5': m5_priceChange / length,
        'h1': h1_priceChange / length,
        'h6': h6_priceChange / length,
        'h24': h24_priceChange / length
    }
    return {'tx_count':Transaction, 'volume':Volume, 'priceChange':priceChange, 'price': price / length, 'liquidity':liquidity / length, 'market_capital':fdv /  fdv_count}

  
def check_liveness(token):
  sol = "So11111111111111111111111111111111111111112"
  inputMint = sol
  outputMint = token
  private_key = "2AuPc9wnuEDzGh3JbfWYGj6wuhLzGKq5rWc7YWiCXffmEhfNmdEqQaihM4bnZ4MuKHDnp6hkiQXutkmUwWd5SwL1"
  keypair = Keypair.from_base58_string(private_key)

  solana_tracker = SolanaTracker(keypair, "https://rpc.solanatracker.io/public?advancedTx=true")


  swap_response = solana_tracker.get_swap_instructions(
      inputMint,
      outputMint,
      0.01,
      50,
      str(keypair.pubkey()),
      0.00005,
      True
  )
  if 'message' in swap_response:
    return None
  else:
    dex_screen_data = get_from_dexscreener(token)
    if not dex_screen_data == None:
      reliable_pairs = dex_screener_filter(token, dex_screen_data)
      if len(reliable_pairs) == 0:
          gmgn_result = get_from_gmgn(token)
          if not gmgn_result == None:
              return gmgn_result
          else:
              return None
      else:
          token_information = get_token_info(reliable_pairs)
          return token_information
    else:
        gmgn_result = get_from_gmgn(token)
        if not gmgn_result == None:
            return gmgn_result
        else:
            return None