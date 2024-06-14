import os
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.expression import func


engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
Base = declarative_base()

tokenlist= [
  { 'name': 'COBRA','address':'ny1koxaJ7hYdZk5KGgbCL4DiUWpmpr5aQH5NJwKpump'},
  { 'name': 'SOLLY','address':'36CEGUfsUU6XXPHPXi62NKXoQ438qN8o1EZM1dgm6DFP'},
  { 'name': '$WIF','address':'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm'},
  { 'name': 'JitoSOL','address':'J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn'},
  { 'name': 'GME','address':'8wXtPeU6557ETkp9WHFY1n1EcU6NxDvbAggHGsMYiHsB'},
  { 'name': 'INF','address':'5oVNBeEEQvYi1cX3ir8Dx5n1P7pdxydbGF2X4TxVusJm'},
  { 'name': 'JUP','address':'JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN'},
  { 'name': 'SLERF','address':'7BgBvyjrZX1YKz4oh9mjb8ZScatkkwb8DzFx7LoiVkM3'},
  { 'name': 'USDT','address':'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB'},
  { 'name': 'SOL','address':'So11111111111111111111111111111111111111112'},
  { 'name': 'JLP','address':'27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4'},
  { 'name': 'USDC','address':'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'},
  { 'name': 'DADDY','address':'4Cnk9EPnW5ixfLZatCPJjDB1PUtcRpVVgTQukm9epump'},
  { 'name': 'PONKE','address':'5z3EqYQo9HiCEs3R84RCDMu2n7anpDMxRhdK8PSWmrRC'},
  { 'name': 'Sphynx','address':'5t4EVfkb5QU8NZXmTzcSK2bQsNWUr2HL64rRb8i6wpat'},
  { 'name': '$DTJR','address':'7G7SMGV9nSG316ykk6iobjMZWa8GZb15Wd25kgaZGTaZ'},
  { 'name': 'DOXXED','address':'BXEapawFFdP9iRv3LGhXC9kfRY91pevzpZnUqsmZpump'},
  { 'name': 'BENDOG','address':'AHW5N8iqZobTcBepkSJzZ61XtAuSzBDcpxtrLG6KUKPk'},
  { 'name': 'BOME','address':'ukHH6c7mMyiWCf1b9pnWe25TSpkDDt3H5pQZgZ74J82'},
  { 'name': 'WETH','address':'7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs'},
  { 'name': 'bSOL','address':'bSo13r4TkiE4KumL71LsHTPpL2euBYLFx6h9HP3piy1'},
  { 'name': 'MEW','address':'MEW1gQWJ3nEXg2qgERiKu7FAFj79PHvQVREQUzScPP5'},
  { 'name': '$michi','address':'5mbK36SZ7J19An8jFochhQS4of8g6BwUjbeCSxBSoWdp'},
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
