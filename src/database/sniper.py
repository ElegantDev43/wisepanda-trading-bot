from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

import config

engine = create_engine(config.DATABASE_URL)

Base = declarative_base()

class Sniper(Base):
    __tablename__ = 'snipers'

    id = Column(Integer, primary_key=True)
    token = Column(String)
    users = Column(JSON)

def initialize():
    Base.metadata.create_all(engine)
