# -*- coding: utf-8 -*-

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

user_var2 = User(username="Zeus", email="frozenzeus86@gmail.com")
session.add(user_var2)
session.commit()

# New Zealand
country_var = Country(name="New Zealand", user=user_var)

session.add(country_var)
session.commit()

highlight_var = Highlight(name="Taupo", 
				prologue="Home to a giant lake.",
				description="Lake Taupo is the largest freshwater lake in Australasia and is roughly the size of Singapore. The lake is the crater of one of the largest volcanic eruptions of the last 5000 years. Lake Taupo is a staggering 159 metres deep. Skydiving is a popular activity in the Taupo area since Taupo has New Zealand's largest commercial skydive drop zone. Taupo is the skydiving capital of the world with more than 30,000 jumps a year.",
				img_url="/static/medium/taupo-460.jpg",
				country=country_var, 
				user=user_var)

session.add(highlight_var)
session.commit()

highlight_var = Highlight(name="Queenstown", 
				prologue="Where boredom is a myth.",
				description="Queenstown is as much a verb as a noun, a place of doing that likes to spruik itself as the 'adventure capital of the world'. It's famously the birthplace of bungy jumping, and the list of adventures you can throw yourself into here is encyclopedic - alpine heliskiing to ziplining. It's rare that a visitor leaves without having tried something that ups their heart rate, but to pigeonhole Queenstown as just a playground is to overlook its cosmopolitan dining and arts scene, its fine vineyards, and the diverse range of bars that can make evenings as fun-filled as the days.",
				img_url="/static/medium/queenstown-460.jpg",
                country=country_var, 
				user=user_var)

session.add(highlight_var)
session.commit()

# Thailand
country_var = Country(name="Thailand", user=user_var2)

session.add(country_var)
session.commit()

highlight_var = Highlight(name="Koh Tao", 
				prologue="Diving paradise on turtle island.",
				description="The island's natural beauty both above and below the water, with its stunning coral reefs and abundant marine life in clear, warm water, bring thousands of visitors here each year making it an unforgettable destination for divers, adventurers and travellers alike. This, combined with the relaxed atmosphere and life style, has been attracting people here for over 40 years and is now a warm second home for many.  Koh Tao has developed in many ways, and with its thriving diving industry, is now one of the leading centres for dive education in the world.",
				img_url="/static/medium/koh-tao-460.jpg",
                country=country_var, 
				user=user_var2)

session.add(highlight_var)
session.commit()

print ("Database populated.")