import os
from sqlalchemy import create_engine, Column, BigInteger, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

import config

engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    chain = Column(String)
    wallets = Column(JSON)

def initialize():
    Base.metadata.create_all(engine)

def create_user(id):
    session = Session()
    if get_user(id) == None:
        chains = config.CHAINS
        wallets = {}
        for chain in chains:
            wallets[chain] = []
        user = User(id=id, chain=chains[0], wallets=wallets)
        session.add(user)
        session.commit()
    session.close()

def get_user(id):
    session = Session()
    user = session.query(User).filter(User.id == id).first()
    session.close()
    return user

def update_user(id, key, value):
    session = Session()
    user = session.query(User).filter(User.id == id).first()
    if key == 'chain':
        user.chain = value
    elif key == 'wallets':
        user.wallets = value
    session.commit()
    session.close()
