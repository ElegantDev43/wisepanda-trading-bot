import requests

api_url = "https://api.dexscreener.com/latest/dex/tokens/5eGcRk6dEXFZj3PLXUhU9nVi13RE8YdE1pQQr5tApump"
response = requests.get(api_url)

data = response.json()

pair_count = len(data['pairs'])

if pair_count == 1:
    print("The token is new: ", pair_count)
else:
    print("The token is old: ", pair_count)