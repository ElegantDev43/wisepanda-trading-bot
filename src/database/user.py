import os
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base


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


def add_by_chat_id(chat_id):
    session = Session()
    user = session.query(User).filter(User.telegram == chat_id).first()
    if user == None:
        chains = config.CHAINS
        wallets = {}
        for chain in chains:
            wallets[chain] = []
        user = User(
            chat_id=chat_id,
            current_chain_index=0,
            wallets=wallets,
            pending_orders=[],
            positions=[],
            session={}
        )
        session.add(user)
        session.commit()
    session.close()


def get_by_chat_id(chat_id):
    session = Session()
    user = session.query(User).filter(User.telegram == chat_id).first()
    session.close()
    return user

def get_user_by_telegram(chat_id):
    session = Session()
    print(chat_id)
    user = session.query(User).filter(User.telegram == chat_id).first()
    session.close()
    return user


def update_by_id(id, key, value):
    session = Session()
    user = session.query(User).filter(User.id == id).first()
    if key == 'current_chain_index':
        user.chain = value
    elif key == 'wallets':
        user.wallets = value
    elif key == 'token_snipers':
        user.token_snipers = value
    elif key == 'pending_orders':
        user.pending_orders = value
    elif key == 'positions':
        user.positions = value
    elif key == 'limit_orders':
        user.limit_orders = value
    elif key == 'dca_orders':
        user.dca_orders = value
    session.commit()
    session.close()
