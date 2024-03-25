from sqlalchemy import create_engine, Column, BigInteger, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

import config

engine = create_engine(config.DATABASE_URL)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    wallet = Column(JSON)
    config = Column(JSON)

def init():
    Base.metadata.create_all(engine)

def exist(id):
    user = get(id)
    return user != None

def create(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = User(id=id, wallet={}, config={'active': False})
    session.add(user)
    session.commit()
    session.close()

def get(id):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = session.query(User).filter(User.id == id).first()
    session.close()
    return user

def update(id, wallet, config):
    Session = sessionmaker(bind=engine)
    session = Session()

    user = User(id=id, wallet={}, config={'active': False})
    session.add(user)
    session.commit()

    session.close()