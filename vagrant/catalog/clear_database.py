from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Country, Highlight

engine = create_engine('sqlite:///countries.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

try:
	session.query(Country).delete()
	session.query(Highlight).delete()
	session.commit()
except:
	session.rollback()