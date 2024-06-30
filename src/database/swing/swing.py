import os
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, JSON, Float
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Swing(Base):
    __tablename__ = 'swing'

    id = Column(Integer, primary_key=True)
    userid = Column(BigInteger)
    chain = Column(String)
    wallet = Column(JSON)
    durations = Column(Integer)
    amount = Column(Float)
    date_current = Column(Integer)
    token = Column(String)
    original_price = Column(Float)
    original_state = Column(String)
    buy_count = Column(Integer)
    sell_count = Column(Integer)
    stop_count = Column(Integer)
    total_count = Column(Integer)
    total_profit = Column(Float)
    total_loss = Column(Float)
    original_amount = Column(Float)
    original_trend = Column(Integer)
    slip_page = Column(Integer)
    take_profit = Column(Integer)
    stop_loss = Column(Integer)
    market_cap = Column(BigInteger)

def initialize():
    Base.metadata.create_all(engine)

def get_all():
    session = Session()
    positions = session.query(Swing).all()
    print("Session::")
    session.close()
    return positions

def get_by_swing_id(id):
    session = Session()
    position = session.query(Swing).filter(Swing.id == id).first()
    session.close()
    return position

def get_by_user_id(user_id):
    session = Session()
    positions = session.query(Swing).filter(Swing.userid == user_id).all()
    session.close()
    return positions

def get_by_user_id_and_token(user_id , address):
    session = Session()
    positions = session.query(Swing).filter(Swing.userid == user_id and Swing.token == address).first()
    session.close()
    return positions

def add_by_user_id(user_id, chain,wallet,durations,amount,token,slippage,market_cap,take_profit,stop_loss):
    session = Session()
    newposition = Swing(
      userid = user_id,
      chain = chain,
      wallet = wallet,
      durations = durations,
      amount = amount,
      date_current = 0,
      token = token,
      original_price = 0,
      original_state = 'sell',
      buy_count = 0,
      sell_count = 0,
      stop_count = 0,
      total_count = 0,
      total_profit = 0,
      total_loss = 0,
      original_amount = amount,
      original_trend = -1,
      slip_page = slippage,
      take_profit = take_profit,
      stop_loss = stop_loss,
      market_cap = market_cap,
    )
    session.add(newposition)
    session.commit()
    session.close()

def update_by_user_id(id,amount,original_price,original_state,buy_count,sell_count,stop_count,total_count,total_profit,total_loss,original_trend):
    session = Session()
    position = session.query(Swing).filter(Swing.id == id).first()
    print("Amounts::",amount,original_price)
    position.amount = amount
    position.original_price = original_price
    position.original_state = original_state
    position.buy_count = buy_count
    position.sell_count = sell_count
    position.stop_count = stop_count
    position.total_count = total_count
    position.date_current = position.date_current + 1
    position.total_profit += total_profit
    position.total_loss += total_loss
    position.original_trend = original_trend
    session.commit()
    session.close()

def remove_by_swing_id(id):
    session = Session()
    position = session.query(Swing).filter(Swing.id == id).first()
    session.delete(position)
    session.commit()
    session.close()
    
def remove_by_userid_and_token(userid,token):
    session = Session()
    position = session.query(Swing).filter(Swing.userid == userid and Swing.token == token).first()
    session.delete(position)
    session.commit()
    session.close()

def get_all_tokens():
    session = Session()
    positions = session.query(Swing).all()
    tokens = []
    for position in positions:
        if position.token in tokens:
            continue
        else:
            tokens.append(position.token)
    session.close()
    return tokens