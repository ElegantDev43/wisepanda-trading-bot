from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

import config

engine = create_engine(config.DATABASE_URL)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    wallet = Column(JSON)
    config = Column(JSON)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

wallet = {
    'chain': 'bsc',
    'address': '0x00',
    'key': '299292'
}
user = User(wallet=wallet, config={'active': False})
session.add(user)
session.commit()

session.close()

print('Done')