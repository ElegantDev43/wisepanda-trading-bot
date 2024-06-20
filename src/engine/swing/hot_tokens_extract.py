import sys
import pandas as pd
import requests
import time
import numpy as np
from scipy.signal import argrelextrema
from datetime import datetime
import matplotlib.pyplot as plt
import dataframe_image as dfi

from src.database.swing import Htokens as HTokens_model

API_KEY = "e6e5d6ab4b3c415d9c691501ee505e06"
X_CHAIN = "solana"

async def exportHotTokens():
#   address = "So11111111111111111111111111111111111111112"

  limit = 50

  url = f"https://public-api.birdeye.so/defi/tokenlist?sort_by=v24hUSD&sort_type=desc&limit={limit}"
  headers = {
      "x-chain": X_CHAIN,
      "X-API-KEY": API_KEY
  }
  response = requests.get(url=url, headers=headers).json()
  inputData = response['data']['tokens']

  index = 0
  for item in inputData:
    item['id'] = index
    item['name'] = item['symbol']
    item['address'] = item['address']
    index = index + 1

  HTokens_model.refresh_hot_tokens(inputData)
