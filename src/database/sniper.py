import os
from sqlalchemy import String, and_, create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Sniper(Base):
    __tablename__ = 'snipers'

    id = Column(Integer, primary_key=True)
    chain = Column(String)
    token = Column(String)
    users = Column(JSON)

def initialize():
    Base.metadata.create_all(engine)

def add_sniper_user_by_token(chain, token, user):
    session = Session()
    sniper = session.query(Sniper).filter(
        and_(
            Sniper.chain == chain,
            Sniper.token == token
        )
    ).first()
    if sniper is not None:
        sniper.users.append(user)
        session.add(sniper)
    else:
        sniper = Sniper(chain=chain, token=token, users=[user])
        session.add(sniper)
    session.commit()
    session.close()

def update_sniper_user_by_token(chain, token, user):
    session = Session()
    sniper = session.query(Sniper).filter(
        and_(
            Sniper.chain == chain,
            Sniper.token == token
        )
    ).first()
    for index in range(len(sniper.users)):
        if sniper.users[index]['id'] == user['id']:
            sniper.users[index] = user
            break
    session.commit()
    session.close()

def cancel_sniper_user_by_token(chain, token, user):
    session = Session()
    sniper = session.query(Sniper).filter(
        and_(
            Sniper.chain == chain,
            Sniper.token == token
        )
    ).first()
    for index in range(len(sniper.users)):
        if sniper.users[index]['id'] == user['id']:
            del sniper.users[index]
            if len(sniper.users) == 0:
                remove_sniper_by_token(chain, token)
            break
    session.commit()
    session.close()

def remove_sniper_by_token(chain, token):
    session = Session()
    sniper = session.query(Sniper).filter(
        and_(
            Sniper.chain == chain,
            Sniper.token == token
        )
    ).first()
    session.delete(sniper)
    session.commit()
    session.close()

def get_sniper_users_by_token(chain, token):
    session = Session()
    sniper = session.query(Sniper).filter(
        and_(
            Sniper.chain == chain,
            Sniper.token == token
        )
    ).first()
    session.close()
    return sniper.users
