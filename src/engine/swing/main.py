import os
import numpy as np
import pandas as pd
import pickle

from src.engine.swing.data_extract import data_extract_main
from src.engine.swing.predict_model import study_model
from src.engine.swing.OrderSystem import OrderSystem,checkTrend
from src.engine.swing.hot_tokens_extract import exportHotTokens
from src.database import swing as swing_model
from src.database import Htokens as HTokens_model

async def Control():
#   addresses = [
#       "So11111111111111111111111111111111111111112",  #Sol
#       "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn",  #JitoSOL
#       "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So", #mSOL
#       "4vqYQTjmKjxrWGtbL2tVkbAU1EVAz9JwcYtd2VE3PbVU", #WYNN
#       "5oVNBeEEQvYi1cX3ir8Dx5n1P7pdxydbGF2X4TxVusJm" #INF
#     ]

  addresses = swing_model.get_all_tokens()

#   await exportHotTokens()

  hot_addresses = HTokens_model.get_all_tokens()

  await data_extract_main(hot_addresses)
  for index in range(0, len(hot_addresses)):
    await study_model(hot_addresses[index])
    print("From Two::Hot Tokens!!!!!")


  for index in range(0,len(hot_addresses)):
    if os.path.exists(f'src/engine/swing/test_data/test_data_{hot_addresses[index]}.csv') != True:
        continue
    dataFrame = pd.read_csv(f'src/engine/swing/test_data/test_data_{hot_addresses[index]}.csv', parse_dates=True, index_col= 2)

    first_data = dataFrame.iloc[-40:]
    first_data = first_data.iloc[::-1]

    if os.path.exists(f'src/engine/swing/model/model_{hot_addresses[index]}_short.pkl') != True:
        predict_model = pickle.load(open(f'src/engine/swing/model/model_short.pkl', 'rb'))
    else:
        predict_model = pickle.load(open(f'src/engine/swing/model/model_{hot_addresses[index]}_short.pkl', 'rb'))
    short_trend = checkTrend(first_data,predict_model)

    if os.path.exists(f'src/engine/swing/model/model_{hot_addresses[index]}_medium.pkl') != True:
        predict_model = pickle.load(open(f'src/engine/swing/model/model_medium.pkl', 'rb'))
    else:
        predict_model = pickle.load(open(f'src/engine/swing/model/model_{hot_addresses[index]}_medium.pkl', 'rb'))
    medium_trend = checkTrend(first_data,predict_model)

    if os.path.exists(f'src/engine/swing/model/model_{hot_addresses[index]}_long.pkl') != True:
        predict_model = pickle.load(open(f'src/engine/swing/model/model_long.pkl', 'rb'))
    else:
        predict_model = pickle.load(open(f'src/engine/swing/model/model_{hot_addresses[index]}_long.pkl', 'rb'))
    long_trend = checkTrend(first_data,predict_model)

    print("YYYY",short_trend,medium_trend,long_trend)
    HTokens_model.update_token_trend(hot_addresses[index],short_trend,medium_trend,long_trend)

  await data_extract_main(addresses)
  print("From One::")
  
  for index in range(0, len(addresses)):
    await study_model(addresses[index])
    print("From Two::")

  positions = swing_model.get_all()
  print("Position::",len(positions))
  for index in range(0,len(positions)):
    current_position = positions[index]
    dataFrame = pd.read_csv(f'src/engine/swing/test_data/test_data_{positions[index].token}.csv', parse_dates=True, index_col= 2)
    dataFrame = dataFrame.iloc[::-1]

    first_data = dataFrame.iloc[-40:]
    amount,original_price,original_state,buy_count,sell_count,stop_count,total_count ,trend, total_profit, total_loss = await OrderSystem(
                current_position.token,
                first_data,current_position.amount,current_position.original_price,
                current_position.original_state,current_position.buy_count,current_position.sell_count,
                current_position.stop_count,current_position.total_count,'medium')
    swing_model.update_by_user_id(id=current_position.id,
                                  amount= amount,
                                  original_price=original_price,
                                  original_state=original_state,
                                  buy_count=buy_count,
                                  sell_count=sell_count,
                                  stop_count=stop_count,
                                  total_count=total_count,
                                  total_profit=total_profit,
                                  total_loss=total_loss)

