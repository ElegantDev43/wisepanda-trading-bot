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

  token_snipers = Column(JSON)
  limit_orders = Column(JSON)
  dca_orders = Column(JSON)
  positions = Column(JSON)
  auto_order = Column(Integer)

def initialize():
	Base.metadata.create_all(engine)

def add(user_id):
	session = Session()
	user = User(
		id=user_id,
		chain=0,
		wallets=[[], [], [], [], [], [], [], [], [], []],
		token_snipers=[],
		limit_orders=[],
		dca_orders=[],
		positions=[],
    auto_order = 0
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
	elif key == 'token_snipers':
		user.token_snipers = value
	elif key == 'limit_orders':
		user.limit_orders = value
	elif key == 'dca_orders':
		user.dca_orders = value
	elif key == 'positions':
		user.positions = value
	elif key == 'auto_order':
		user.auto_order = value
	session.commit()
	session.close()