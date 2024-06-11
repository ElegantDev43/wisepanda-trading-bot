import os
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.expression import func


engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
Base = declarative_base()


class HTokens(Base):
    __tablename__ = 'HTokens'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    short_signal = Column(Integer)
    medium_signal = Column(Integer)
    long_signal = Column(Integer)


def initialize():
    Base.metadata.create_all(engine)

def get_hot_tokens(limit):
    session = Session()
    sh_bul_tokens = session.query(HTokens).filter(HTokens.short_signal == 1).limit(limit).all()
    if len(sh_bul_tokens) < limit:
        sh_bul_tokens = session.query(HTokens).filter(HTokens.short_signal == 0).order_by(func.random()).limit(limit).all()

    sh_bea_tokens = session.query(HTokens).filter(HTokens.short_signal == -1).limit(limit).all()
    if len(sh_bea_tokens) < limit:
        sh_bea_tokens = session.query(HTokens).filter(HTokens.short_signal == 0).order_by(func.random()).limit(limit).all()

    me_bul_tokens = session.query(HTokens).filter(HTokens.medium_signal == 1).limit(limit).all()
    if len(me_bul_tokens) < limit:
        me_bul_tokens = session.query(HTokens).filter(HTokens.medium_signal == 0).order_by(func.random()).limit(limit).all()

    me_bea_tokens = session.query(HTokens).filter(HTokens.medium_signal == -1).limit(limit).all()
    if len(me_bea_tokens) < limit:
        me_bea_tokens = session.query(HTokens).filter(HTokens.medium_signal == 0).order_by(func.random()).limit(limit).all()

    lo_bul_tokens = session.query(HTokens).filter(HTokens.long_signal == 1).limit(limit).all()
    if len(lo_bul_tokens) < limit:
        lo_bul_tokens = session.query(HTokens).filter(HTokens.long_signal == 0).order_by(func.random()).limit(limit).all()

    lo_bea_tokens = session.query(HTokens).filter(HTokens.long_signal == -1).limit(limit).all()
    if len(lo_bea_tokens) < limit:
        lo_bea_tokens = session.query(HTokens).filter(HTokens.long_signal == 0).order_by(func.random()).limit(limit).all()

    session.close()
    return sh_bul_tokens,sh_bea_tokens,me_bul_tokens,me_bea_tokens,lo_bul_tokens,lo_bea_tokens

def get_all_tokens():
    session = Session()
    tokens = session.query(HTokens).all()
    addresses = []
    for token in tokens:
        addresses.append(token.address)
    session.close()
    return addresses

def refresh_hot_tokens(new_tokens):
    session = Session()
    tokens = session.query(HTokens).all()
    for token in tokens:
        session.delete(token)
    for token in new_tokens:
        newtoken = HTokens(
            id = token['id'] + 1,
            name = token['symbol'],
            address = token['address'],
            short_signal = 0,
            medium_signal = 0,
            long_signal = 0,
        )
        session.add(newtoken)
    session.commit()
    session.close()

def update_token_trend(address,short,medium,long):
    session = Session()
    token = session.query(HTokens).filter(HTokens.address == address).first()
    token.short_signal = int(short)
    token.medium_signal = int(medium)
    token.long_signal = int(long)
    session.commit()
    session.close()
