import os
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
Base = declarative_base()

chainss = ['ethereum', 'solana', 'base']

key_index = ['buy', 'gas', 'sell']
default_buy_amounts = [0.1, 0.3, 0.5, 1.0]
default_gas_amounts = [0.1, 0.3, 0.5]
default_sell_amounts = [10, 30, 50, 100]


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger)
    current_chain_index = Column(Integer)
    wallets = Column(JSON)
    token_snipers = Column(JSON)
    pending_orders = Column(JSON)
    positions = Column(JSON)
    limit_orders = Column(JSON)
    dca_orders = Column(JSON)
    keyboards = Column(JSON)


def initialize():
    Base.metadata.create_all(engine)


def add_by_chat_id(chat_id):
    session = Session()
    user = session.query(User).filter(User.chat_id == chat_id).first()
    if user == None:
        chains = chainss
        wallets = {}
        keyboards = {}
        for chain in chains:
            wallets[chain] = []
        for index in key_index:
            if index == 'buy':
                keyboards[index] = default_buy_amounts
            elif index == 'sell':
                keyboards[index] = default_sell_amounts
            elif index == 'gas':
                keyboards[index] = default_gas_amounts
        user = User(
            chat_id=chat_id,
            current_chain_index=0,
            wallets=wallets,
            pending_orders=[],
            limit_orders=[],
            dca_orders=[],
            positions=[],
            token_snipers=[],
            keyboards=keyboards
        )
        session.add(user)
        session.commit()
    session.close()


def get_by_chat_id(chat_id):
    session = Session()
    user = session.query(User).filter(User.chat_id == chat_id).first()
    session.close()
    return user


def update_by_id(id, key, value):
    session = Session()
    user = session.query(User).filter(User.id == id).first()
    if key == 'current_chain_index':
        user.current_chain_index = value
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
    elif key == 'keyboards':
        user.keyboards = value
    session.commit()
    session.close()
