from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Country, Highlight

engine = create_engine('sqlite:///countries.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

try:
    session.query(User).delete()
    session.query(Country).delete()
    session.query(Highlight).delete()
    session.commit()
except BaseException:
    session.rollback()
