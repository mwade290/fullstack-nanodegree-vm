# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Country, Highlight

engine = create_engine('sqlite:///countries.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Add user
user_var = User(username="Mark Wade", email="mwade290@gmail.com")
session.add(user_var)
session.commit()

# New Zealand
country_var = Country(name="New Zealand", user=user_var)

session.add(country_var)
session.commit()

highlight_var = Highlight(name="Taupo",
                          prologue="Home to a giant lake.",
                          description=("Lake Taupo is the largest freshwater lake in Australasia and is roughly the size of Singapore. The lake is the crater of one of the largest volcanic eruptions of the last 5000 years. Lake Taupo is a staggering 159 metres deep. Skydiving is a popular activity in the Taupo area since Taupo has New Zealand's largest commercial skydive drop zone. Taupo is the skydiving capital of the world with more than 30,000 jumps a year."),
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
country_var = Country(name="Thailand", user=user_var)

session.add(country_var)
session.commit()

highlight_var = Highlight(name="Koh Tao",
                          prologue="Diving paradise on turtle island.",
                          description="The island's natural beauty both above and below the water, with its stunning coral reefs and abundant marine life in clear, warm water, bring thousands of visitors here each year making it an unforgettable destination for divers, adventurers and travellers alike. This, combined with the relaxed atmosphere and life style, has been attracting people here for over 40 years and is now a warm second home for many.  Koh Tao has developed in many ways, and with its thriving diving industry, is now one of the leading centres for dive education in the world.",
                          img_url="/static/medium/koh-tao-460.jpg",
                          country=country_var,
                          user=user_var)

session.add(highlight_var)
session.commit()

highlight_var = Highlight(name="Bangkok",
                          prologue="Same same, but different.",
                          description="Bangkok welcomes more visitors than any other city in the world and it doesn't take long to realise why. Bangkok is a city of contrasts with action at every turn. Marvel at the gleaming temples, catch a tuk tuk along the bustling Chinatown or take a longtail boat through floating markets. Food is another Bangkok highlight, from local dishes served at humble street stalls to haute cuisine at romantic rooftop restaurants. Luxury malls compete with a sea of boutiques and markets, where you can treat yourself without overspending. Extravagant Luxury hotels and surprisingly cheap serviced apartments welcome you with the same famed Thai hospitality. And no visit to Bangkok would be complete without a glimpse of its famous nightlife. Be it nightclubs, cabarets or exotic red-light districts, Bangkok never ceases to amaze. ",
                          img_url="/static/medium/bangkok-460.jpg",
                          country=country_var,
                          user=user_var)

session.add(highlight_var)
session.commit()

# Malaysia
country_var = Country(name="Malaysia", user=user_var)

session.add(country_var)
session.commit()

highlight_var = Highlight(name="George Town",
                          prologue="Bursting with culture and heritage.",
                          description="Over 500 years, George Town has grown from a small Malaysian village to what it is today. During that time, influences of Asia and Europe have endowed this city with a unique multicultural heritage that can be witnessed around every corner. With all the gorgeous history around town, in 2008, George Town was awarded UNESCO World Heritage Site status. Georgetown has over 12,000 old buildings consisting of Chinese shophouses, residential jetties, churches, temples, mosques and grand British colonial government offices and monuments. Most of these buildings are condensed in the Lebuh Acheh historical enclave making it easy to explore on foot.",
                          img_url="/static/medium/george-town-460.jpg",
                          country=country_var,
                          user=user_var)

session.add(highlight_var)
session.commit()

highlight_var = Highlight(name="Cameron Highlands",
                          prologue="Where it's always time for tea.",
                          description="Emerald tea plantations unfurl across valleys, and the air is freshened by eucalyptus - Malaysia's largest hill-station area feels instantly restorative. Temperatures in these 1300m to 1829m heights rarely top 30 degrees Celsius, inspiring convoys of weekenders to sip tea and eat strawberries here.",
                          img_url="/static/medium/cameron-highlands-460.jpg",
                          country=country_var,
                          user=user_var)

session.add(highlight_var)
session.commit()

# Peru
country_var = Country(name="Peru", user=user_var)

session.add(country_var)
session.commit()

highlight_var = Highlight(name="Machu Picchu",
                          prologue="Incredible historic world of the Incas.",
                          description="For many visitors to Peru and even South America, a visit to the Inca city of Machu Picchu is the long-anticipated highpoint of their trip. In a spectacular location, it's the best-known archaeological site on the continent. This awe-inspiring ancient city was never revealed to the conquering Spaniards and was virtually forgotten until the early part of the 20th century.",
                          img_url="/static/medium/machu-picchu-460.jpg",
                          country=country_var,
                          user=user_var)

session.add(highlight_var)
session.commit()

# Isle Of Man
country_var = Country(name="Isle Of Man", user=user_var)

session.add(country_var)
session.commit()

highlight_var = Highlight(name="The Great Laxey Wheel",
                          prologue="Largest working waterwheel.",
                          description="This feat of Victorian engineering and ingenuity is the largest surviving waterwheel of its kind in the world. The Lady Isabella as she is also known, served the mine for 70 years and became the Island's most dramatic tourist attraction. Watch the mighty wheel turn and climb to the top for panoramic views across Glen Mooar Valley. Beyond the wheel take an hour to explore the mine and the trail to the mine ruins to learn more about the lives of the Laxey miners.",
                          img_url="/static/medium/laxey-wheel-460.jpg",
                          country=country_var,
                          user=user_var)

session.add(highlight_var)
session.commit()

highlight_var = Highlight(name="TT Races",
                          prologue="Longest running road race in the world.",
                          description="There is nothing on Earth quite like the Isle of Man TT Races. No other motorcycle race is held on such a challenging track as the 37-mile plus Mountain Course with its seemingly never-ending series of bends. The skill, bravery and concentration levels required are immense, with speeds approaching 200mph, and, while difficult to learn and even harder to come first, the rewards for winning on the world famous course are like no other. No other motorsport event can boast more than 100 years of such illustrious history, rich in tradition and legends, and to have your name inscribed on a TT trophy is to sit with the gods.",
                          img_url="/static/medium/tt-460.jpg",
                          country=country_var,
                          user=user_var)

session.add(highlight_var)
session.commit()

highlight_var = Highlight(name="Tynwald",
                          prologue="Longest continuous running parliament in the world.",
                          description="Dating back to Viking origins over one thousand years ago, Tynwald (in Manx - Ard-whaiyl Tinvaal) is the oldest continuous legislature in the world. On 5th July each year, Tynwald Court assembles in the open air on Tynwald Hill at St John's - a Viking site of the Manx Parliament - to conduct parliamentary business and receive petitions for redress. It debates matters of policy, approves delegated legislation adopts financial motions.",
                          img_url="/static/medium/tynwald-460.jpg",
                          country=country_var,
                          user=user_var)

session.add(highlight_var)
session.commit()

# Italy
country_var = Country(name="Italy", user=user_var)

session.add(country_var)
session.commit()

highlight_var = Highlight(name="The Colosseum",
                          prologue="Roman gladiator battleground.",
                          description="The Colosseum was a setting for something beyond gladiatorial amusements, however, utilized likewise for open executions and legendary plays. The Romans would frequently re-authorize celebrated military triumphs, with free confirmation and sustenance for all guests. Maybe the most stupendous occasions at the Colosseum, however, was the sea fights in the overflowed field. The main sea fight at the Colosseum was held in 80 AD, amid the field's opening function. Ruler Titus requested the amphitheater to be overflowed and had extraordinary level bottomed boats intended to oblige for the shallow water. Students of history still don't know how precisely these ocean fights were composed, however, the boats utilized at the field were likely little copies of genuine Roman boats.",
                          img_url="/static/medium/colosseum-460.jpg",
                          country=country_var,
                          user=user_var)

session.add(highlight_var)
session.commit()

# Ireland
country_var = Country(name="Ireland", user=user_var)

session.add(country_var)
session.commit()

highlight_var = Highlight(name="Galway",
                          prologue="Where the craic is mighty.",
                          description="Arty, bohemian Galway (Gaillimh) is one of Ireland's most engaging cities. Brightly painted pubs heave with live music, while restaurants and cafes offer front-row seats for observing buskers and street theatre. Remnants of the medieval town walls lie between shops selling handcrafted Claddagh rings, books and musical instruments, bridges arch over the salmon-stuffed River Corrib, and a long promenade leads to the seaside suburb of Salthill, on Galway Bay, the source of the area's famous oysters.",
                          img_url="/static/medium/galway-460.jpg",
                          country=country_var,
                          user=user_var)

session.add(highlight_var)
session.commit()

print("Database populated.")
