import requests

api_url = "https://api.dexscreener.com/latest/dex/tokens/5eGcRk6dEXFZj3PLXUhU9nVi13RE8YdE1pQQr5tApump" 
response = requests.get(api_url)

data = response.json()

pairs = data.get('pairs', [])

min_price = float('inf')
min_price_dexId = ""
max_price = float('-inf')
max_price_dexId = ""

for pair in pairs:
    price = float(pair.get('priceUsd', 0))
    dex_id = pair.get('dexId', '')

    if price < min_price:
        min_price = price
        min_price_dexId = dex_id

    if price > max_price:
        max_price = price
        max_price_dexId = dex_id

print(f"Minimum Price: {min_price:.10f}, dexId: {min_price_dexId}")
print(f"Maximum Price: {max_price:.10f}, dexId: {max_price_dexId}")