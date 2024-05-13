
from datetime import datetime
import time
import matplotlib.pyplot as plt
from uniswap import fetch_trading_price_history,fetch_trading_amount_history
from indicators import calculate_RSI,calculate_SMA,calculate_EMA

# Example usage
trading_pair = "0x8f0cb37cdff37e004e0088f563e5fe39e05ccc5b"  # Example pair: WBTC/UNI
trading_pair_one = "0x9db9e0e53058c89e5b94e29621a205198648425b" # Example pair:WBTC/USDT
trading_pair_two = "0xcbcdf9626bc03e24f779434178a73a0b4bad62ed" # Example pair:WBTC/WETH

token_Elon = "0x761d38e5ddf6ccf6cf7c55759d5210750b5d60f3" #Exampe: Elon
token_WETH = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2" #Example: WETH

limit = 5  # Number of recent swaps to fetch

print("Hello")
current_timestamp = int(time.time())
print(current_timestamp)

RSI_Period = 14
MA_Period = 14
MACD_Short_Period, MACD_Long_Period, Signal_Period = 12,26,9

start_date = "2024-03-21"

Max_Period = max(RSI_Period,MA_Period,MACD_Long_Period,MACD_Long_Period,Signal_Period)
print("Max Period:",Max_Period)

date_format = "%Y-%m-%d"  # Format of the date string
# Convert the date string to a datetime object
date_object = datetime.strptime(start_date, date_format)
# Convert the datetime object to a Unix timestamp (integer)
timestamp = int(date_object.timestamp()) - 86400 * Max_Period
new_start_date = datetime.fromtimestamp(timestamp).strftime(date_format)
print("Start Date:",new_start_date)

trading_price_history = fetch_trading_price_history(new_start_date,trading_pair,limit,current_timestamp)
trading_amount_history = fetch_trading_amount_history(token_Elon,token_WETH,limit,current_timestamp)

# Extract token0Price values and corresponding dates
token0_prices = [float(entry['token0Price']) for entry in trading_price_history]
dates = [datetime.utcfromtimestamp(entry['date']) for entry in trading_price_history]

# Calculate RSI values
#rsi_values = [calculate_RSI(token0_prices[i:i+14]) for i in range(len(token0_prices) - 14)]
rsi_values = calculate_RSI(token0_prices)
sma_values = calculate_SMA(token0_prices)
ema_values = calculate_EMA(token0_prices)

# last_rsi_value = rsi_values[-1]
# rsi_values.extend([last_rsi_value] * (len(token0_prices) - len(rsi_values)))
  
print(len(sma_values))
print(len(ema_values))

dates = dates[Max_Period:]
show0_prices = token0_prices[Max_Period:]
rsi_values = rsi_values[Max_Period:]
sma_values = sma_values[Max_Period:]
ema_values = ema_values[Max_Period:]

# Plotting the token0Price chart

# plt.figure(figsize=(10, 6))

fig, axs = plt.subplots(2,1)  # Create 2 subplots (2 rows)
axs[0].plot(dates, show0_prices, marker='o', linestyle='-', color='blue', label='price')
axs[0].plot(dates, sma_values, label='SMA', color='green')
axs[0].plot(dates, ema_values, label='EMA', color='red')
axs[0].set_title('Token0 Price Chart(WBTC/UNI)')
axs[0].set_xlabel('Date')
axs[0].set_ylabel('Token0 Price')
axs[0].legend()
axs[0].grid(True)

#plt.plot(dates, token0_prices, marker='o', linestyle='-')
axs[1].plot(dates, rsi_values, label='RSI', color='green')
axs[1].set_title('RSI Chart(WBTC/UNI)')
axs[1].set_xlabel('Date')
axs[1].set_ylabel('RSI')
axs[1].legend()
axs[1].grid(True)

# Adjust layout
plt.tight_layout()

plt.show()


# if trading_price_history:
#     for swap in trading_price_history:
#         date = datetime.datetime.utcfromtimestamp(swap['date'])

#         print("Date:", date)
#         print("token0Price:", swap['token0Price'])
#         print("token1Price:", swap['token1Price'])
#         print("volumeToken0:", swap['volumeToken0'])
#         print("volumeToken1:", swap['volumeToken1'])
#         # print("Timestamp:", swap['timestamp'])
#         print("-------------------------------------------")

# if trading_amount_history:
#     for swap in trading_amount_history:
#         date = datetime.datetime.utcfromtimestamp(int(swap['timestamp']))

#         print("Date:", date)
#         print("amount0:", swap['amount0'])
#         print("amount1:", swap['amount1'])
#         # print("Timestamp:", swap['timestamp'])
#         print("-------------------------------------------")