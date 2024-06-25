import os
import asyncio

from src.database.swing import swing as swing_model
from src.database.swing import Htokens as htokens_model
from src.database import user as user_model

from src.engine.swing.data_extract import exportTestValues

chain_name = ['solana','ethereum']

tokenlist= [
  { 'name': '$WIF','address':'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm'},
  { 'name': 'JitoSOL','address':'J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn'},
  { 'name': 'INF','address':'5oVNBeEEQvYi1cX3ir8Dx5n1P7pdxydbGF2X4TxVusJm'},
  { 'name': 'JLP','address':'27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4'},
  { 'name': 'PONKE','address':'5z3EqYQo9HiCEs3R84RCDMu2n7anpDMxRhdK8PSWmrRC'},
  { 'name': 'WETH','address':'7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs'},
  { 'name': 'bSOL','address':'bSo13r4TkiE4KumL71LsHTPpL2euBYLFx6h9HP3piy1'},
  #{ 'name': 'Trump','address':'Cmg4dyhnnUcWmakmyKQZ7MHEdcuCgoKa8iXKE8Nknjiv'},
]

def getTokenImage(token):
  if os.path.exists(f'src/engine/swing/data_png/prices_{token}.png') != True:
    asyncio.run(exportTestValues(token))
  image_path = f'src/engine/swing/data_png/prices_{token}.png'
  
  return image_path

def addAutoToken(userid,token,amount,wallet):
  
  user = user_model.get(userid)
  chain = user.chain

  swing_model.add_by_user_id(userid,chain_name[chain],wallet,
                             50,amount,token)

def getAutoTokens(userid):
  autoTokens = swing_model.get_by_user_id(userid)
  return autoTokens

def remove_by_userid_and_token(userid,token):
  swing_model.remove_by_userid_and_token(userid,token)

def SetFullyAutoTokens(type,userid,amount,wallet):
  
  if type == 'Start':  
    user = user_model.get(userid)
    chain = user.chain

    token_count = len(tokenlist)

    for token in tokenlist:
      swing_model.add_by_user_id(userid,chain_name[chain],wallet,
                                50,amount / token_count ,token['address'])
    return 'OK'
  elif type == 'Stop':
    for token in tokenlist:
      position = swing_model.get_by_user_id_and_token(userid,token['address'])
      if position.original_state == 'buy':
        print(f'Sell {token['address']}')
      swing_model.remove_by_swing_id(position.id)
    return 'OK'
  elif type == 'Market Status':
    total_amount = 0
    original_amount = 0
    for token in tokenlist:
      position = swing_model.get_by_user_id_and_token(userid,token['address'])
      total_amount = total_amount + position.amount
      original_amount = original_amount + position.original_amount
    
    return total_amount, original_amount
  elif type == 'Auto Status':
    positions = swing_model.get_by_user_id(userid)
    if len(positions) > 0:
      return 'Stop'
    return 'Start'