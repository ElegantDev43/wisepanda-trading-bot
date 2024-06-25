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
  limit_orders = Column(JSON)
  dca_orders = Column(JSON)
  auto_order = Column(JSON)

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
        'limit': 100,
        'count': 0,
      },
      'lp': {
        'active': False,
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
    limit_orders=[],
    dca_orders=[],
    auto_order=auto_order
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
  elif key == 'limit_orders':
    user.limit_orders = value
  elif key == 'dca_orders':
    user.dca_orders = value
  elif key == 'auto_order':
    user.auto_order = value
  session.commit()
  session.close()