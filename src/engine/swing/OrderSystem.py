import os
import numpy as np
import pandas as pd

from tti.indicators import BollingerBands,SwingIndex,RelativeStrengthIndex,MovingAverage,EaseOfMovement
from tti.indicators import MovingAverageConvergenceDivergence,OnBalanceVolume,WilliamsR,VolumeOscillator
from tti.indicators import ChandeMomentumOscillator,DetrendedPriceOscillator,DirectionalMovementIndex
from tti.indicators import LinearRegressionIndicator,LinearRegressionSlope,MedianPrice,Momentum
from tti.indicators import PriceRateOfChange,StandardDeviation,StochasticMomentumIndex,WildersSmoothing
from tti.indicators import IchimokuCloud,ParabolicSAR,CommodityChannelIndex,OnBalanceVolume,PriceAndVolumeTrend
from tti.indicators import TimeSeriesForecast

import pickle

from sklearn.metrics import accuracy_score, classification_report



def checkTrend(prices,predict_model):

  if len(prices) < 40:
      return 0

  ind_swing = 0
  swing_indicator = SwingIndex(input_data=prices)
  ind_swing = swing_indicator.getTiValue()[0]

  rsi_indicator = RelativeStrengthIndex(input_data=prices)
  ind_rsi = rsi_indicator.getTiValue()[0]

  sma_indicator = MovingAverage(input_data=prices,period=5)
  ind_sma_5 = sma_indicator.getTiValue()[0]

  sma_indicator = MovingAverage(input_data=prices,period=10)
  ind_sma_10 = sma_indicator.getTiValue()[0]

  sma_indicator = MovingAverage(input_data=prices,period=20)
  ind_sma_20 = sma_indicator.getTiValue()[0]

  sma_indicator = MovingAverage(input_data=prices,period=40)
  ind_sma_40 = sma_indicator.getTiValue()[0]

  ema_indicator = MovingAverage(input_data=prices,ma_type='exponential' , period=5)
  ind_ema_5 = ema_indicator.getTiValue()[0]

  ema_indicator = MovingAverage(input_data=prices,ma_type='exponential' , period=10)
  ind_ema_10 = ema_indicator.getTiValue()[0]

  ema_indicator = MovingAverage(input_data=prices,ma_type='exponential' , period=20)
  ind_ema_20 = ema_indicator.getTiValue()[0]

  ema_indicator = MovingAverage(input_data=prices,ma_type='exponential' , period=40)
  ind_ema_40 = ema_indicator.getTiValue()[0]

  tma_indicator = MovingAverage(input_data=prices,ma_type='triangular')
  ind_tma = tma_indicator.getTiValue()[0]

  macd_indicator = MovingAverageConvergenceDivergence(input_data=prices)
  ind_macd = macd_indicator.getTiValue()[0]
  ind_signal = macd_indicator.getTiValue()[1]

  bb_indicator = BollingerBands(input_data=prices)
  ind_bb_up = bb_indicator.getTiValue()[0]
  ind_bb_low = bb_indicator.getTiValue()[1]

  william_indicator = WilliamsR(input_data=prices)
  ind_william = william_indicator.getTiValue()[0]

  volume_indicator = VolumeOscillator(input_data=prices)
  ind_vol = volume_indicator.getTiValue()[0]

  onvolume_indicator = OnBalanceVolume(input_data=prices)
  ind_onvolume = onvolume_indicator.getTiValue()[0]

  cmo_indicator = ChandeMomentumOscillator(input_data=prices)
  ind_cmo = cmo_indicator.getTiValue()[0]

  dpo_indicator = DetrendedPriceOscillator(input_data=prices)
  ind_dpo = dpo_indicator.getTiValue()[0]

  dmi_indicator = DirectionalMovementIndex(input_data=prices)
  ind_dmi_plusdi = dmi_indicator.getTiValue()[0]
  ind_dmi_minusdi = dmi_indicator.getTiValue()[1]
  ind_dmi_dx = dmi_indicator.getTiValue()[2]
  ind_dmi_adx = dmi_indicator.getTiValue()[3]
  ind_dmi_adxr = dmi_indicator.getTiValue()[4]

  lri_indicator = LinearRegressionIndicator(input_data=prices)
  ind_lri = lri_indicator.getTiValue()[0]

  lrs_indicator = LinearRegressionSlope(input_data=prices)
  ind_lrs = lrs_indicator.getTiValue()[0]

  mp_indicator = MedianPrice(input_data=prices)
  ind_mp = mp_indicator.getTiValue()[0]

  mom_indicator = Momentum(input_data=prices)
  ind_mom = mom_indicator.getTiValue()[0]

  prc_indicator = PriceRateOfChange(input_data=prices)
  ind_prc = prc_indicator.getTiValue()[0]

  sd_indicator = StandardDeviation(input_data=prices)
  ind_sd = sd_indicator.getTiValue()[0]

  smi_indicator = StochasticMomentumIndex(input_data=prices)
  ind_smi = smi_indicator.getTiValue()[0]

  ws_indicator = WildersSmoothing(input_data=prices)
  ind_ws = ws_indicator.getTiValue()[0]
  
  ICloud_indicator = IchimokuCloud(input_data=prices)
  ind_tenkan_sen = ICloud_indicator.getTiValue()[0]
  ind_kijun_sen = ICloud_indicator.getTiValue()[1]
  ind_senkou_a = ICloud_indicator.getTiValue()[2]
  ind_senkou_b = ICloud_indicator.getTiValue()[3]

  sar_indicator = ParabolicSAR(input_data=prices)
  ind_sar = sar_indicator.getTiValue()[0]

  cci_indicator = CommodityChannelIndex(input_data=prices)
  ind_cci = cci_indicator.getTiValue()[0]

  obv_indicator = OnBalanceVolume(input_data=prices)
  ind_obv = obv_indicator.getTiValue()[0]

  pvt_indicator = PriceAndVolumeTrend(input_data=prices)
  ind_pvt = pvt_indicator.getTiValue()[0]

  tsf_indicator = TimeSeriesForecast(input_data=prices)
  ind_tsf = tsf_indicator.getTiValue()[0]

#   eom_indicator = EaseOfMovement(input_data=prices)
#   ind_emv = eom_indicator.getTiValue()[0]
  if(np.isnan(ind_swing)):
      ind_swing = 0
  if(np.isnan(ind_rsi)):
      ind_rsi = 0
  if(np.isnan(ind_tma)):
      ind_tma = 0
  if(np.isnan(ind_macd)):
      ind_macd = 0
  if(np.isnan(ind_signal)):
      ind_signal = 0
  if(np.isnan(ind_bb_up)):
      ind_bb_up = 0
  if(np.isnan(ind_bb_low)):
      ind_bb_low = 0
  if(np.isnan(ind_william)):
      ind_william = 0
  if(np.isnan(ind_vol)):
      ind_vol = 0
  if(np.isnan(ind_onvolume)):
      ind_onvolume = 0
  if(np.isnan(ind_cmo)):
      ind_cmo = 0
  if(np.isnan(ind_dpo)):
      ind_dpo = 0
  if(np.isnan(ind_dmi_plusdi)):
      ind_dmi_plusdi = 0
  if(np.isnan(ind_dmi_minusdi)):
      ind_dmi_minusdi = 0
  if(np.isnan(ind_dmi_dx)):
      ind_dmi_dx = 0
  if(np.isnan(ind_dmi_adx)):
      ind_dmi_adx = 0
  if(np.isnan(ind_dmi_adxr)):
      ind_dmi_adxr = 0

  if(np.isnan(ind_lri)):
      ind_lri = 0
  if(np.isnan(ind_lrs)):
      ind_lrs = 0
  if(np.isnan(ind_mp)):
      ind_mp = 0
  if(np.isnan(ind_mom)):
      ind_mom = 0
  if(np.isnan(ind_prc)):
      ind_prc = 0

  if(np.isnan(ind_sd)):
      ind_sd = 0
  if(np.isnan(ind_smi)):
      ind_smi = 0
  if(np.isnan(ind_ws)):
      ind_ws = 0

  X_test = np.array([[
                     ind_sma_5,ind_ema_5,ind_tma,
                     ind_swing,ind_rsi,ind_macd,ind_signal,
                     ind_william,ind_vol,ind_onvolume,
                     ind_cmo,ind_dpo,ind_dmi_plusdi,ind_dmi_minusdi,ind_dmi_dx,ind_dmi_adx,ind_dmi_adxr,
                     ind_lrs,ind_mom,ind_prc,ind_sd,ind_smi,
                     ind_tenkan_sen,ind_kijun_sen,ind_senkou_a,ind_senkou_b,ind_sar,ind_cci,ind_obv,ind_pvt,
                     ind_tsf
                     ]])

  X_test_scaled = X_test

  print(X_test_scaled)

  y_result = predict_model.predict(X_test_scaled)

  print(y_result)
  return y_result[0]

async def OrderSystem(token,prices,amount,original_price,original_state,buy_count,sell_count,stop_count,total_count,period,original_trend):
  profit = 0
  loss = 0
  action = 'hold'

  if os.path.exists(f'src/engine/swing/model/model_{token}.pkl') != True:
    if os.path.exists(f'src/engine/swing/model/model.pkl') != True:
      return    
    predict_model = pickle.load(open(f'src/engine/swing/model/model.pkl', 'rb'))
  else:
    predict_model = pickle.load(open(f'src/engine/swing/model/model_{token}.pkl', 'rb'))

  if len(prices) < 40:
      return amount,original_price,original_state,buy_count,sell_count,stop_count,total_count,original_trend,profit,loss

  trend = checkTrend(prices,predict_model)

  current_price = prices[['close'][0]].iloc[39]
  divergence = prices[['close'][0]].iloc[39] - prices[['close'][0]].iloc[38]

  if original_trend == 1 and trend == -1 and original_state == 'buy' and current_price > original_price:
      original_state = 'sell'
      profit = amount * (current_price / original_price - 1)
      amount = amount * (current_price / original_price)
      original_price = 0
      sell_count = sell_count + 1
      total_count = total_count + 1
      action = 'sell'

  elif original_trend == -1 and trend == 1 and original_state == 'sell':
      original_state = 'buy'
      original_price = current_price
      buy_count = buy_count + 1
      total_count = total_count + 1
      action = 'buy'

  if original_state == 'buy' and current_price < (original_price * 98.0 / 100):
      loss = amount * (current_price / original_price - 1)
      amount = amount *  (current_price / original_price)
      original_state = 'sell'
      original_price = 0
      stop_count = stop_count + 1
      total_count = total_count + 1
      action = 'sell'

  return action,amount,original_price,original_state,buy_count,sell_count,stop_count,total_count,trend , profit, loss