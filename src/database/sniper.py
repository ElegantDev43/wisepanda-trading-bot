import os
from sqlalchemy import String, and_, create_engine, Column, Integer, JSON, func
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Sniper(Base):
    __tablename__ = 'snipers'

    id = Column(Integer, primary_key=True)
    token = Column(JSON)
    users = Column(JSON)

def initialize():
    Base.metadata.create_all(engine)

def get_sniper_by_token(token):
    session = Session()
    sniper = session.query(Sniper).filter(
        and_(
            func.cast(Sniper.token['chain'], String) == token['chain'],
            func.cast(Sniper.token['address'], String) == token['address']
        )
    ).first()
    session.close()
    return sniper

def add_sniper_user_by_token(token, user):
    session = Session()
    sniper = get_sniper_by_token(token)
    if sniper != None:
        sniper.users.append(user)
    else:
        sniper = Sniper(token=token, users=[user])
        session.add(sniper)
    session.commit()
    session.close()

def update_sniper_user_by_token(token, user):
    session = Session()
    sniper = get_sniper_by_token(token)
    for index in range(len(sniper.users)):
        if sniper.users[index]['id'] == user['id']:
            sniper.users[index] = user
            break
    session.commit()
    session.close()

def cancel_sniper_user_by_token(token, user):
    session = Session()
    sniper = get_sniper_by_token(token)
    for index in range(len(sniper.users)):
        if sniper.users[index]['id'] == user['id']:
            del sniper.users[index]
            if len(sniper.users) == 0:
                remove_sniper_by_token(token)
            break
    session.commit()
    session.close()

def remove_sniper_by_token(token):
    session = Session()
    sniper = get_sniper_by_token(token)
    session.delete(sniper)
    session.commit()
    session.close()

def get_sniper_users_by_token(token):
    session = Session()
    sniper = get_sniper_by_token(token)
    session.close()
    return sniper.users
