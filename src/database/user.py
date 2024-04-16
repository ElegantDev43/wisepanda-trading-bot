import os
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

import config

engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram = Column(BigInteger)
    chain = Column(String)
    wallets = Column(JSON)
    orders = Column(JSON)
    positions = Column(JSON)
    session = Column(JSON)

def initialize():
    Base.metadata.create_all(engine)

def create_user_by_telegram(telegram):
    session = Session()
    if get_user_by_telegram(telegram) == None:
        chains = config.CHAINS
        wallets = {}
        for chain in chains:
            wallets[chain] = []
        user = User(telegram=telegram, chain=chains[0], wallets=wallets, orders=[], positions=[], session={})
        session.add(user)
        session.commit()
    session.close()

def get_user_by_telegram(telegram):
    session = Session()
    user = session.query(User).filter(User.telegram == telegram).first()
    session.close()
    return user

def get_user_by_id(id):
    session = Session()
    user = session.query(User).filter(User.id == id).first()
    session.close()
    return user

def update_user_by_id(id, key, value):
    session = Session()
    user = session.query(User).filter(User.id == id).first()
    if key == 'chain':
        user.chain = value
    elif key == 'wallets':
        user.wallets = value
    elif key == 'orders':
        user.orders = value
    elif key == 'positions':
        user.positions = value
    elif key == 'session':
        user.session = value
    session.commit()
    session.close()

def get_session_by_id(id):
    session = Session()
    user = get_user_by_id(id)
    session.close()
    return user.session
