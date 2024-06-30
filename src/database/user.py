import os
from sqlalchemy import create_engine, Column, Integer, BigInteger, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
  __tablename__ = 'users'

  id = Column(BigInteger, primary_key=True)
  chain = Column(Integer)
  wallets = Column(JSON)

  positions = Column(JSON)
  auto_sniper = Column(JSON)
  token_snipers = Column(JSON)
  lp_snipers = Column(JSON)
  limit_orders = Column(JSON)
  dca_orders = Column(JSON)
  auto_order = Column(JSON)
  user_feature_values = Column(JSON)
  auto_swing_status = Column(Integer)
def initialize():
  Base.metadata.create_all(engine)

def gets():
  session = Session()
  users = session.query(User).all()
  session.close()
  return users

def add(user_id):
  session = Session()
  wallets = []
  auto_sniper = []
  auto_order = []
  user_feature_values = {
        'token_sniper_auto':{
          'wallet_row':1,
          'wallet':0,
          'amount':-999,
          'slippage':-999,
          'stop-loss':0,
          'min_market_cap':0,
          'max_market_cap':0,
          'chain_auto_sell_params':[]
        },
        'token_sniper_manual':{
          'token':'',
          'wallet_row':1,
          'wallet':0,
          'amount':0,
          'slippage':0,
          'stop-loss':0,
          'chain_auto_sell_params':[]
        },
        'buyer':{
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
        'swing_auto':{
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
  for _ in range(10):
    wallets.append([])
    auto_sniper.append({
      'token': {
        'active': False,
        'amount': 1,
        'slippage': 50,
        'wallet_id': 0,
        'auto_sell': [],
        'min_market_capital': 1000,
        'max_market_capital': 10000,
        'stop_loss':0
      },
      'lp': {
        'active': False,
        'amount': 1,
        'slippage': 50,
        'wallet_id': 0
      }
    })
    auto_order.append({
      'buy': {
        'active': False,
        'amount': 1,
        'slippage': 10,
      },
      'sell': {
        'active': False,
        'amount': 50,
        'slippage': 10
      }
    })
  user = User(
    id=user_id,
    chain=0,
    wallets=wallets,
    positions=[],
    auto_sniper=auto_sniper,
    token_snipers=[],
    lp_snipers=[],
    limit_orders=[],
    dca_orders=[],
    auto_order=auto_order,
    user_feature_values=user_feature_values,
    auto_swing_status=0
  )
  session.add(user)
  session.commit()
  session.close()

def get(user_id):
  session = Session()
  user = session.query(User).filter(User.id == user_id).first()
  session.close()
  return user

def set(user_id, key, value):
  session = Session()
  user = session.query(User).filter(User.id == user_id).first()
  if key == 'chain':
    user.chain = value
  elif key == 'wallets':
    user.wallets = value
  elif key == 'positions':
    user.positions = value
  elif key == 'auto_sniper':
    user.auto_sniper = value
  elif key == 'token_snipers':
    user.token_snipers = value
  elif key == 'lp_snipers':
    user.lp_snipers = value
  elif key == 'limit_orders':
    user.limit_orders = value
  elif key == 'dca_orders':
    user.dca_orders = value
  elif key == 'auto_order':
    user.auto_order = value
  elif key == 'user_feature_values':
    user.user_feature_values = value
  elif key == 'auto_swing_status':
    user.auto_swing_status = value
  session.commit()
  session.close()