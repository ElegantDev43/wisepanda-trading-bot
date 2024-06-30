from src.database import api as user_api

user = {
  "id":"",
  "token_sniper_auto":{
    'wallet_row':1,
    'wallet':0,
    'amount':-999,
    'slippage':-999,
    'stop-loss': 0,
    'min_market_cap':0,
    'max_market_cap':0,
    'chain_auto_sell_params':[]
  },
  "token_sniper_manual":{
    'token':'',
    'wallet_row':1,
    'wallet':0,
    'amount':-999,
    'slippage':-999,
    'stop-loss':0,
    'chain_auto_sell_params':[]
  },
  "buyer":{
    'order_name':0,
    'token':'',
    'wallet_row':1,
    'wallet':0,
    'amount':-999,
    'slippage':-999,
    'stop-loss':0,
    'max_market_capital':0,
    'interval':0,
    'count':0
  },
  "seller":{
    'order_name':0,
    'token':'',
    'wallet_row':1,
    'wallet':0,
    'amount':-999,
    'slippage':-999,
    'profit':0,
    'interval':0,
    'count':0
  },
  "swing_auto":{
    'order_name':0,
    'token':'',
    'wallet_row':1,
    'wallet':0,
    'amount':-999,
    'slippage':-999,
    'take-profit':0,
    'stop-loss':0,
    'market_capital':0
  },
  "swing_manual":{
    'token':'',
    'wallet_row':1,
    'wallet':0,
    'amount':-999,
    'slippage':-999,
    'stop-loss':0
  }
}


def get_user_feature_values(chat_id, feature):
  keyboard = user_api.get_user_feature_values(chat_id)
  return keyboard[feature]

def update_user_feature_values(chat_id, feature, update_values):
  user_api.set_user_feature_values(chat_id, feature, update_values)
  
def initialize_values(chat_id, feature):
  user_api.set_user_feature_values(chat_id, feature, user[feature])