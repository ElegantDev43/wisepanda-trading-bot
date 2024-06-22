import os
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.expression import func
import random



engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
Base = declarative_base()

tokenlist= [
  { 'name': '$WIF','address':'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm'},
  { 'name': 'JitoSOL','address':'J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn'},
  { 'name': 'INF','address':'5oVNBeEEQvYi1cX3ir8Dx5n1P7pdxydbGF2X4TxVusJm'},
  { 'name': 'USDT','address':'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB'},
  { 'name': 'SOL','address':'So11111111111111111111111111111111111111112'},
  { 'name': 'JLP','address':'27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4'},
  { 'name': 'USDC','address':'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'},
  { 'name': 'PONKE','address':'5z3EqYQo9HiCEs3R84RCDMu2n7anpDMxRhdK8PSWmrRC'},
  { 'name': 'WETH','address':'7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs'},
  { 'name': 'bSOL','address':'bSo13r4TkiE4KumL71LsHTPpL2euBYLFx6h9HP3piy1'},
  { 'name': 'Trump','address':'Cmg4dyhnnUcWmakmyKQZ7MHEdcuCgoKa8iXKE8Nknjiv'},
  { 'name': 'FTX','address':'5raTruYd7sCnoGvb8t8V8H6rWpT9eFVm9NhQoqu3nb6E'},
  { 'name': 'ADOGE','address':'6SEJ69LQNmE7ZErThw2dSh1mUvAdwMrb6BzEQSCb5NTt'},
  { 'name': 'SEEDS','address':'BtRNWtzHLetGSL6XS2s2d1vH1wYE8LcEq4fvSWTnVDBD'},
  { 'name': 'CLASSIC','address':'AbytHkeCbiorVGpvEQ6mjUoaty6Dn29m8sr33iphGRvb'},
  { 'name': 'POOH','address':'HywPTRhGDBXFK2eT11fq7GFyi6DtThQ4eNHopC69sK1Q'},
  { 'name': 'TUTI','address':'9vCHEfjcNCt2ktWEeLNhMAuf2UifJeBfCB8f1n6niY5U'},
  { 'name': 'POGBA','address':'sBm8ykqoGQKtE72vXCKf4oCU9zsGcM6NJZa4xZjMM58'},
  { 'name': 'NULL','address':'3R6cwKMQRF5D791FLHFp9Dnnxgd4oEjj9Xi3dn7SwC7R'},
  { 'name': 'LOL','address':'EAjdnmDgdnDt1qacYZRXkEyMufJfszzw9BxUv7bdJtoM'},
  { 'name': 'SOCK','address':'HQJcySEuhzyT9UuCj2YfynMC19pAuviSU34aKK3uoAsQ'},
  { 'name': 'XNX','address':'EPM1iQwm5p3ABYZJWnCo1hvVCaDVEWTGDHjSyCTnVFAA'},
]

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

    for token in tokenlist:
      add_hot_tokens(token['name'],token['address'])

def add_hot_tokens(name, address):
    session = Session()
    token = session.query(HTokens).filter(HTokens.address == address).all()
    if len(token) < 1:
      newtoken = HTokens(
        name = name,
        address = address,
        short_signal = 0,
        medium_signal = 0,
        long_signal = 0
      )
      session.add(newtoken)
    session.commit()
    session.close()

def get_top_hot_token():
  random_integer = random.randint(1, len(tokenlist))
  
  return tokenlist[random_integer]['address']

def get_token_name_by_address(address):
  for token in tokenlist:
    if token['address'] == address:
      return token['name']
  
  default = 'Null'
  return default

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
