import numpy as np
import pandas as pd

from src.engine.swing.data_extract import data_extract_main
from src.engine.swing.predict_model import study_model
from src.engine.swing.OrderSystem import OrderSystem
from src.database import swing as swing_model


async def Control():
  addresses = [
      "So11111111111111111111111111111111111111112",  #Sol
      "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn",  #JitoSOL
      "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So", #mSOL
      "4vqYQTjmKjxrWGtbL2tVkbAU1EVAz9JwcYtd2VE3PbVU", #WYNN
      "5oVNBeEEQvYi1cX3ir8Dx5n1P7pdxydbGF2X4TxVusJm" #INF
    ]
  
  await data_extract_main(addresses)
  print("From One::")
  
  for index in range(0, len(addresses)):
    await study_model(addresses[index])
    print("From Two::")

  positions = swing_model.get_all()
  print("Position::",len(positions))
  for index in range(0,len(positions)):
    current_position = positions[index]
    dataFrame = pd.read_csv('src/engine/swing/test_data/test_data.csv', parse_dates=True, index_col= 2)
    dataFrame = dataFrame.iloc[::-1]

    first_data = dataFrame.iloc[-40:]
    amount,original_price,original_state,buy_count,sell_count,stop_count,total_count = await OrderSystem(
                current_position.token,
                first_data,current_position.amount,current_position.original_price,
                current_position.original_state,current_position.buy_count,current_position.sell_count,
                current_position.stop_count,current_position.total_count)
    swing_model.update_by_user_id(id=current_position.id,
                                  amount= amount,
                                  original_price=original_price,
                                  original_state=original_state,
                                  buy_count=buy_count,
                                  sell_count=sell_count,
                                  stop_count=stop_count,
                                  total_count=total_count)

