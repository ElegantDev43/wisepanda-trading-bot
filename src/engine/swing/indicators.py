import backtrader as bt
import numpy as np
import pandas as pd

def calculate_RSI(prices, period=14):

    rsi_values = []
    for i in range(0, period):
        sample_prices = prices[0:i]

        delta = np.diff(sample_prices)
        gain = np.where(delta >= 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = np.mean(gain[:period])
        avg_loss = np.mean(loss[:period])

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsi_values.append(rsi)

    for i in range(len(prices) - 14):
        sample_prices = prices[i:i+14]

        delta = np.diff(sample_prices)
        gain = np.where(delta >= 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = np.mean(gain[:period])
        avg_loss = np.mean(loss[:period])

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsi_values.append(rsi)
    return rsi_values

def calculate_SMA(prices,  period=14):
    sma_values = []

    for i in range(0, period - 1):
        sma = sum(prices[:i]) / (i+1)
        sma_values.append(sma)

    for i in range(len(prices) - period + 1):
        window = prices[i:i+period]
        sma = sum(window) / period
        sma_values.append(sma)
    return sma_values

def calculate_EMA(prices, period=14):
    ema_values = []
    multiplier = 2 / (period + 1)
    for i in range(0, period):
        ema = sum(prices[:i]) / (i+1)
        ema_values.append(ema)

    for i in range(period, len(prices)):
        ema = (prices[i] - ema) * multiplier + ema
        ema_values.append(ema)
    return ema_values


def calculate_MACD(prices, short_period=12, long_period=26, signal_period=9):
    short_ema = calculate_EMA(prices, short_period)
    long_ema = calculate_EMA(prices, long_period)

    macd_line = [short_ema[i] - long_ema[i] for i in range(len(short_ema))]

    signal_line = calculate_EMA(macd_line, signal_period)

    return macd_line, signal_line


def calculate_vol(prices, volumes):
    obv_values = [0]  # Initialize the OBV values with 0

    for i in range(1, len(prices)):
        # if prices[i] > prices[i - 1]:
        #     obv_values.append(obv_values[-1] + volumes[i])  # Add volume if price increases
        # elif prices[i] < prices[i - 1]:
        #     obv_values.append(obv_values[-1] - volumes[i])  # Subtract volume if price decreases
        # else:
        #     obv_values.append(obv_values[-1])  # If price remains unchanged, OBV remains the same
        obv_values.append(volumes[i]);

    return obv_values


def calculate_bollinger_bands(prices, window=20, num_std=2):
    # Calculate rolling mean (middle band)
    middle_values = []
    upper_values = []
    lower_values = []

    df = pd.DataFrame(prices)

    # Calculate rolling mean (middle band)
    middle_band = df.rolling(window=window).mean()

    # Calculate rolling standard deviation
    std_dev = df.rolling(window=window).std()

    # Calculate upper band
    upper_band = middle_band + (std_dev * num_std)

    # Calculate lower band
    lower_band = middle_band - (std_dev * num_std)


    # for i in range(0, len(prices)):
    #     middle_band = prices[i].rolling(window=window).mean()
    #     # Calculate rolling standard deviation
    #     std_dev = prices[i].rolling(window=window).std()
    #     # Calculate upper band
    #     upper_band = middle_band + (std_dev * num_std)
    #     # Calculate lower band
    #     lower_band = middle_band - (std_dev * num_std)

    #     middle_values.append(middle_band)
    #     upper_values.append(upper_band)
    #     lower_values.append(lower_band)

    print(middle_band , upper_band, lower_band)

    return middle_band, upper_band, lower_band


def calculate_stochastic_oscillator(prices, n=14, m=3):
    percent_k_array = []
    percent_d_array = []

    for i in range(len(prices)):
        if i >= n - 1:
            # Calculate lowest low and highest high over n periods
            lowest_low = min(prices[i - n + 1:i + 1])
            highest_high = max(prices[i - n + 1:i + 1])

            # Calculate %K
            current_close = prices[i]
            percent_k = ((current_close - lowest_low) / (highest_high - lowest_low)) * 100

            # Append %K to percent_k_array
            percent_k_array.append(percent_k)

            # Calculate %D (moving average of %K over m periods)
            if i >= n + m - 2:
                percent_d = sum(percent_k_array[-m:]) / m
                percent_d_array.append(percent_d)
            else:
                percent_d_array.append(None)
        else:
            percent_k_array.append(None)
            percent_d_array.append(None)

    return percent_k_array, percent_d_array