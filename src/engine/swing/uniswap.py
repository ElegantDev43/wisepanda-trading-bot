import requests
from datetime import datetime



def fetch_trading_price_history(start_date,trading_pair,limit = 10, current_time = None):
    date_format = "%Y-%m-%d"  # Format of the date string

    # Convert the date string to a datetime object
    date_object = datetime.strptime(start_date, date_format)

    # Convert the datetime object to a Unix timestamp (integer)
    timestamp = int(date_object.timestamp())

    # GraphQL query to fetch trading history for a specific pair in Uniswap V3
    query = """
    {
        poolDayDatas(
            where: {
            pool: "%s",
            date_gte:  %s,
            date_lt: %s
            }
        ) {
            date
            token0Price
            token1Price
            volumeToken0
            volumeToken1
            tvlUSD
            sqrtPrice
            volumeUSD
        }
    }
    """ % (trading_pair,timestamp,current_time)

    # Define the Uniswap V3 subgraph endpoint
    url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'

    # Make the HTTP POST request
    response = requests.post(url, json={'query': query})

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # print(data)
        return data['data']['poolDayDatas']
    else:
        print('Failed to fetch data:', response.status_code)
        return None

def fetch_trading_amount_history(trading_token0, trading_token1,limit = 10, current_time = None):
    # GraphQL query to fetch trading history for a specific pair in Uniswap V3
    query = """
    {
       swaps(
            where: {
            token0: "%s",
            token1: "%s",
            timestamp_gte: 1710995200,
            timestamp_lt: %s
            }
        ) {
            id
            timestamp
            amount0
            amount1
        }
    }
    """ % (trading_token0,trading_token1,current_time)

    # Define the Uniswap V3 subgraph endpoint
    url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'

    # Make the HTTP POST request
    response = requests.post(url, json={'query': query})

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # print(data)
        return data['data']['swaps']
    else:
        print('Failed to fetch data:', response.status_code)
        return None