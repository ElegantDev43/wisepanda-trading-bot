import os
from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Sniper(Base):
    __tablename__ = 'snipers'

    token = Column(String, primary_key=True)
    users = Column(JSON)

def initialize():
    Base.metadata.create_all(engine)

def add_sniper(token, user):
    session = Session()
    sniper = session.query(Sniper).filter(Sniper.token == token).first()
    if sniper != None:
        sniper.users.append(user)
    else:
        sniper = Sniper(token=token, users=[user])
        session.add(sniper)
    session.commit()
    session.close()

def update_sniper(token, user):
    session = Session()
    sniper = session.query(Sniper).filter(Sniper.token == token).first()
    for index in range(len(sniper.users)):
        if sniper.users[index]['id'] == user['id']:
            sniper.users[index] = user
            break
    session.commit()
    session.close()

def cancel_sniper(token, user):
    session = Session()
    sniper = session.query(Sniper).filter(Sniper.token == token).first()
    for index in range(len(sniper.users)):
        if sniper.users[index]['id'] == user['id']:
            del sniper.users[index]
            if len(sniper.users) == 0:
                remove_token(token)
            break
    session.commit()
    session.close()

def remove_token(token):
    session = Session()
    sniper = session.query(Sniper).filter(Sniper.token == token).first()
    session.delete(sniper)
    session.commit()
    session.close()

def get_tokens():
    session = Session()
    tokens = session.query(Sniper.token).all()
    session.close()
    return tokens

def get_users(token):
    session = Session()
    sniper = session.query(Sniper).filter(Sniper.token == token).first()
    session.close()
    return sniper.users
