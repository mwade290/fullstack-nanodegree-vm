from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Country, Highlight

engine = create_engine('sqlite:///countries.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

user_var = User(username="Mark Wade", email="mwade290@gmail.com")
session.add(user_var)
session.commit()

# New Zealand
country_var = Country(name="New Zealand", user=user_var)

session.add(country_var)
session.commit()

highlight_var = Highlight(name="Taupo", 
				description="Home to a lake the size of Singapore.",
                country=country_var, 
				user=user_var)

session.add(highlight_var)
session.commit()

highlight_var = Highlight(name="Queenstown", 
				description="Where boredem is a myth.",
                country=country_var, 
				user=user_var)

session.add(highlight_var)
session.commit()

user_var = User(username="Zeus", email="frozenzeus86@gmail.com")
session.add(user_var)
session.commit()

# Thailand
country_var = Country(name="Thailand", user=user_var)

session.add(country_var)
session.commit()

highlight_var = Highlight(name="Koh Tao", 
				description="Diving paradise.",
                country=country_var, 
				user=user_var)

session.add(highlight_var)
session.commit()

print ("Database populated.")