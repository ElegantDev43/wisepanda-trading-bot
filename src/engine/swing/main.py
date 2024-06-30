import threading
import asyncio
import os
import numpy as np
import pandas as pd
import pickle

from src.engine.swing.data_extract import data_extract_main
from src.engine.swing.predict_model import study_model
from src.engine.swing.OrderSystem import OrderSystem,checkTrend
from src.engine.swing.hot_tokens_extract import exportHotTokens
from src.database.swing import swing as swing_model
from src.database.swing import Htokens as HTokens_model

from src.engine import swap as swap_engine
from src.engine.chain import dex as dex_engine


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

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

  # hot_addresses = HTokens_model.get_all_tokens()

  # await data_extract_main(hot_addresses)
  # for index in range(0, len(hot_addresses)):
  #   await study_model(hot_addresses[index])
  #   print("From Two::Hot Tokens!!!!!")

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
    action,amount,original_price,original_state,buy_count,sell_count,stop_count,total_count ,trend, total_profit, total_loss = await OrderSystem(
                current_position.token,
                first_data,current_position.amount,current_position.original_price,
                current_position.original_state,current_position.buy_count,current_position.sell_count,
                current_position.stop_count,current_position.total_count,'medium',current_position.original_trend,
                current_position.take_profit,current_position.stop_loss)
  
    userid = current_position.userid
    chain = current_position.chain
    token = current_position.token
    amount = current_position.amount
    wallet = current_position.wallet
    slippage = current_position.slip_page
    stop_loss = current_position.stop_loss
    if action == 'sell':
      amount = 100

    dex_engine.swap(0, action, token, amount, slippage, wallet)

    swing_model.update_by_user_id(id = current_position.id,
                                  amount = amount,
                                  original_price = original_price,
                                  original_state = original_state,
                                  buy_count = buy_count,
                                  sell_count = sell_count,
                                  stop_count = stop_count,
                                  total_count = total_count,
                                  total_profit = total_profit,
                                  total_loss = total_loss,
                                  original_trend = trend)
    


async def updateData():
    while True:
        await Control()
    # await Control()


def run_update_data_in_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(updateData())
    loop.close()

def initialize():
    print('Starting the engine...')
    thread  = threading.Thread(target=run_update_data_in_thread)
    thread.start()

