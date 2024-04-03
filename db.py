from sqlalchemy import create_engine, Column, BigInteger, JSON, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

import config

engine = create_engine(config.DATABASE_URL)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    wallet = Column(JSON)
    configuration = Column(JSON)
    active = Column(Boolean)

def init():
    Base.metadata.create_all(engine)

def create(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    if get(id) == None:
        user = User(id=id, wallet={}, configuration={}, active=False)
        session.add(user)
        session.commit()
    session.close()

def get(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter(User.id == id).first()
    session.close()
    return user

def save(id, wallet, configuration, active):
    Session = sessionmaker(bind=engine)
    session = Session()

    user = session.query(User).filter(User.id == id).first()
    if wallet:
        user.wallet = wallet
    elif configuration:
        user.configuration = configuration
    else:
        user.active = active
    session.commit()

    session.close()