import os
import sys
import pandas as pd
import requests
import time
import numpy as np
from scipy.signal import argrelextrema
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import dataframe_image as dfi
from tti.indicators import BollingerBands,SwingIndex,RelativeStrengthIndex,MovingAverage,EaseOfMovement
from tti.indicators import MovingAverageConvergenceDivergence,OnBalanceVolume,WilliamsR,VolumeOscillator
from tti.indicators import ChandeMomentumOscillator,DetrendedPriceOscillator,DirectionalMovementIndex
from tti.indicators import LinearRegressionIndicator,LinearRegressionSlope,MedianPrice,Momentum
from tti.indicators import PriceRateOfChange,StandardDeviation,StochasticMomentumIndex,WildersSmoothing
from tti.indicators import IchimokuCloud,ParabolicSAR,CommodityChannelIndex,OnBalanceVolume,PriceAndVolumeTrend
from tti.indicators import TimeSeriesForecast

from src.engine.swing.lstm_model import study_lstm

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

API_KEY = "e6e5d6ab4b3c415d9c691501ee505e06"
X_CHAIN = "solana"

#startAt = "2023-11-29 00:00:00"
startAt = "2023-10-29 00:00:00"
endAt = "2024-03-28 00:00:00"
starttestAt = "2024-03-29 00:00:00"
endtestAt = "2024-05-30 00:00:00"
interval = "15m"

async def exportTechnicalIndicators(address):
  addressType = "token"

  today = datetime.now()
  two_months_before = today - relativedelta(months=2)
  two_months_before = two_months_before.strftime("%Y-%m-%d %H:%M:%S")

  timeFrom = int(time.mktime(time.strptime(startAt, '%Y-%m-%d %H:%M:%S')))
#  timeTo = int(time.mktime(time.strptime(endAt, '%Y-%m-%d %H:%M:%S')))
  timeTo = int(time.mktime(time.strptime(two_months_before, '%Y-%m-%d %H:%M:%S')))

  print(timeFrom, timeTo,address)

  url = f"https://public-api.birdeye.so/defi/history_price?address={address}&address_type={addressType}&type={interval}&time_from={timeFrom}&time_to={timeTo}"
  headers = {
      "x-chain": X_CHAIN,
      "X-API-KEY": API_KEY
  }
  response = requests.get(url=url, headers=headers).json()
  inputData = response['data']['items']

  if inputData == [] or len(inputData) < 1000:
      return

  index = 0
  for item in inputData:
    unixTime = datetime.fromtimestamp(item['unixTime'])
    item['id'] = index
    item['Date'] = unixTime.strftime("%Y-%m-%d")
    item['High'] = item['value']
    item['Low'] = item['value']
    item['open'] = item['value']
    item['adj close'] = item['value']
    item['volume'] = item['value']
    item['close'] = item['value']
    index = index + 1

  dataFrame = pd.DataFrame.from_dict(inputData, orient='columns')
  dataFrame.index = pd.DatetimeIndex(dataFrame['unixTime'])

  dataFrame = dataFrame.drop(columns=['unixTime'])

  dataFrame.ffill(inplace=True)
  dataFrame.bfill(inplace=True)

  swing_indicator = SwingIndex(input_data=dataFrame)
  dataFrame['Swing'] = swing_indicator.getTiData()

  rsi_indicator = RelativeStrengthIndex(input_data=dataFrame)
  dataFrame['RSI'] = rsi_indicator.getTiData()

  sma_indicator = MovingAverage(input_data=dataFrame,period = 5)
  dataFrame['SMA_5'] = sma_indicator.getTiData()

  sma_10_indicator = MovingAverage(input_data=dataFrame,period = 10)
  dataFrame['SMA_10'] = sma_indicator.getTiData()

  sma_indicator = MovingAverage(input_data=dataFrame,period = 20)
  dataFrame['SMA_20'] = sma_indicator.getTiData()

  sma_indicator = MovingAverage(input_data=dataFrame,period = 40)
  dataFrame['SMA_40'] = sma_indicator.getTiData()

  ema_indicator = MovingAverage(input_data=dataFrame,ma_type='exponential',period=5)
  dataFrame['EMA_5'] = ema_indicator.getTiData()

  ema_indicator = MovingAverage(input_data=dataFrame,ma_type='exponential',period=10)
  dataFrame['EMA_10'] = ema_indicator.getTiData()

  ema_indicator = MovingAverage(input_data=dataFrame,ma_type='exponential',period=20)
  dataFrame['EMA_20'] = ema_indicator.getTiData()

  ema_indicator = MovingAverage(input_data=dataFrame,ma_type='exponential',period=40)
  dataFrame['EMA_40'] = ema_indicator.getTiData()

  tsma_indicator = MovingAverage(input_data=dataFrame,ma_type='time_series')
  dataFrame['TSMA'] = tsma_indicator.getTiData()
  
  tma_indicator = MovingAverage(input_data=dataFrame,ma_type='triangular')
  dataFrame['TMA'] = tma_indicator.getTiData()

  macd_indicator = MovingAverageConvergenceDivergence(input_data=dataFrame)
  dataFrame['MACD'] = macd_indicator.getTiData()[['macd'][0]]
  dataFrame['Signal'] = macd_indicator.getTiData()[['signal_line'][0]]

  bb_indicator = BollingerBands(input_data=dataFrame)
  dataFrame['bb_up'] = bb_indicator.getTiData()[['upper_band'][0]]
  dataFrame['bb_low'] = bb_indicator.getTiData()[['lower_band'][0]]

  william_indicator = WilliamsR(input_data=dataFrame)
  dataFrame['william'] = william_indicator.getTiData()

  volume_indicator = VolumeOscillator(input_data=dataFrame)
  dataFrame['vol'] = volume_indicator.getTiData()
  
  onvolume_indicator = OnBalanceVolume(input_data=dataFrame)
  dataFrame['OnVolume'] = onvolume_indicator.getTiData()
  
  adl_indicator = ChandeMomentumOscillator(input_data=dataFrame)
  dataFrame['cmo'] = adl_indicator.getTiData()[['cmo'][0]]

  dpo_indicator = DetrendedPriceOscillator(input_data=dataFrame)
  dataFrame['dpo'] = dpo_indicator.getTiData()[['dpo'][0]]

  lri_indicator = LinearRegressionIndicator(input_data=dataFrame)
  dataFrame['lri'] = lri_indicator.getTiData()[['lri'][0]]

  lrs_indicator = LinearRegressionSlope(input_data=dataFrame)
  dataFrame['lrs'] = lrs_indicator.getTiData()[['lrs'][0]]

  mp_indicator = MedianPrice(input_data=dataFrame)
  dataFrame['mp'] = mp_indicator.getTiData()[['mp'][0]]

  mom_indicator = Momentum(input_data=dataFrame)
  dataFrame['mom'] = mom_indicator.getTiData()[['mom'][0]]

  prc_indicator = PriceRateOfChange(input_data=dataFrame)
  dataFrame['prc'] = prc_indicator.getTiData()[['prc'][0]]

  smi_indicator = StandardDeviation(input_data=dataFrame)
  dataFrame['sd'] = smi_indicator.getTiData()[['sd'][0]]

  smi_indicator = StochasticMomentumIndex(input_data=dataFrame)
  dataFrame['smi'] = smi_indicator.getTiData()[['smi'][0]]

  ws_indicator = WildersSmoothing(input_data=dataFrame)
  dataFrame['ws'] = ws_indicator.getTiData()[['ws'][0]]

  ICloud_indicator = IchimokuCloud(input_data=dataFrame)
  dataFrame['tenkan_sen'] = ICloud_indicator.getTiData()[['tenkan_sen'][0]]
  dataFrame['kijun_sen'] = ICloud_indicator.getTiData()[['kijun_sen'][0]]
  dataFrame['senkou_a'] = ICloud_indicator.getTiData()[['senkou_a'][0]]
  dataFrame['senkou_b'] = ICloud_indicator.getTiData()[['senkou_b'][0]]

  sar_indicator = ParabolicSAR(input_data=dataFrame)
  dataFrame['sar'] = sar_indicator.getTiData()[['sar'][0]]

  cci_indicator = CommodityChannelIndex(input_data=dataFrame)
  dataFrame['cci'] = cci_indicator.getTiData()[['cci'][0]]

  obv_indicator = OnBalanceVolume(input_data=dataFrame)
  dataFrame['obv'] = obv_indicator.getTiData()[['obv'][0]]

  pvt_indicator = PriceAndVolumeTrend(input_data=dataFrame)
  dataFrame['pvt'] = pvt_indicator.getTiData()[['pvt'][0]]

  tsf_indicator = TimeSeriesForecast(input_data=dataFrame)
  dataFrame['tsf'] = tsf_indicator.getTiData()[['tsf'][0]]

  dmi_indicator = DirectionalMovementIndex(input_data=dataFrame)
  dmi_data = dmi_indicator.getTiData()
  dataFrame['+di'] = dmi_data['+di']
  dataFrame['-di'] = dmi_data['-di']
  dataFrame['dx'] = dmi_data['dx']
  dataFrame['adx'] = dmi_data['adx']
  dataFrame['adxr'] = dmi_data['adxr']

  date_range = [2,5,10]


  for date_num in range(0,len(date_range)):
    dataFrame[f'Target_{date_range[date_num]}'] = np.where(
        dataFrame['id']
    ,0,1)

    # Add target variable for price direction
    dataFrame[f'Target_{date_range[date_num]}'] = np.where(dataFrame['close'].shift(date_range[date_num]) > dataFrame['close'], -1, 1)
    dataFrame[f'Target_{date_range[date_num]}'] = dataFrame[f'Target_{date_range[date_num]}'].shift(-date_range[date_num])


  dataFrame = dataFrame.iloc[::-1]

  dataFrame = dataFrame.dropna()

  dataFrame.to_csv(f'src/engine/swing/price_data/price_data_{address}.csv', index=False)

  print(dataFrame)

async def SaveAsGraph(dataFrame,address):
    # Plot the DataFrame
    plt.figure(figsize=(10, 5))
    plt.plot(dataFrame['Date'], dataFrame['value'], linestyle='-')

    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Sample DataFrame Plot')

    # Save the plot as a PNG file
    plt.savefig(f'src/engine/swing/data_png/prices_{address}.png')

async def exportTestValues(address):
#   address = "So11111111111111111111111111111111111111112"

  addressType = "token"

  today = datetime.now()
  formatted_today = today.strftime("%Y-%m-%d %H:%M:%S")
  two_months_before = today - relativedelta(months=2)
  two_months_before = two_months_before.strftime("%Y-%m-%d %H:%M:%S")
  print("Today is:",formatted_today)

  timeFrom = int(time.mktime(time.strptime(two_months_before, '%Y-%m-%d %H:%M:%S')))
  timeTo = int(time.mktime(time.strptime(formatted_today, '%Y-%m-%d %H:%M:%S')))

  url = f"https://public-api.birdeye.so/defi/history_price?address={address}&address_type={addressType}&type={'1D'}&time_from={timeFrom}&time_to={timeTo}"
  headers = {
      "x-chain": X_CHAIN,
      "X-API-KEY": API_KEY
  }
  response = requests.get(url=url, headers=headers).json()
  inputData = response['data']['items']

  index = 0
  for item in inputData:
    unixTime = datetime.fromtimestamp(item['unixTime'])
    item['id'] = index
    item['Date'] = unixTime.strftime("%Y-%m-%d")
    item['High'] = item['value']
    item['Low'] = item['value']
    item['open'] = item['value']
    item['adj close'] = item['value']
    item['volume'] = item['value']
    item['close'] = item['value']
    index = index + 1

  if inputData == []:
      return

  dataFrame = pd.DataFrame.from_dict(inputData, orient='columns')
  dataFrame.index = pd.DatetimeIndex(dataFrame['unixTime'])

  dataFrame = dataFrame.drop(columns=['unixTime'])

  dataFrame = dataFrame.iloc[::-1]

  dataFrame = dataFrame.dropna()

  dataFrame.to_csv(f"src/engine/swing/test_data/test_data_{address}.csv", index=False)

  # Save the DataFrame as a PNG image
  await SaveAsGraph(dataFrame,address)
  await study_lstm(address)

async def data_extract_main(addresses):

  if not os.path.exists('src/engine/swing/test_data'):
        os.makedirs('src/engine/swing/test_data')
  if not os.path.exists('src/engine/swing/price_data'):
        os.makedirs('src/engine/swing/price_data')
  if not os.path.exists('src/engine/swing/model'):
        os.makedirs('src/engine/swing/model')
  if not os.path.exists('src/engine/swing/data_png'):
        os.makedirs('src/engine/swing/data_png')

  for index in range(0, len(addresses)):
    await exportTechnicalIndicators(addresses[index])
    print("Test_data_Done")
    await exportTestValues(addresses[index])
    print("Technical_data_Done")
