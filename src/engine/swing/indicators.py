import backtrader as bt
import numpy as np

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