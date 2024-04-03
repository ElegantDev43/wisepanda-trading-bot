from sqlalchemy import create_engine, Column, BigInteger, JSON, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

import src.config as config

engine = create_engine(config.DATABASE_URL)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    chain = Column(String)
    wallets = Column(JSON)
    configuration = Column(JSON)
    active = Column(Boolean)

def initialize():
    Base.metadata.create_all(engine)

def create_user(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    if get_user(id) == None:
        user = User(id=id, chain='', wallets={}, configuration={}, active=False)
        session.add(user)
        session.commit()
    session.close()

def get_user(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter(User.id == id).first()
    session.close()
    return user

def update_user(id, key, value):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter(User.id == id).first()
    if key == 'chain':
        user.chain = value
    elif key == 'wallets':
        user.wallets = value
    elif key == 'configuration':
        user.configuration = value
    elif key == 'active':
        user.active = value
    session.commit()
    session.close()