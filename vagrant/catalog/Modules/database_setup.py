import os
import sys
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	username = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	picture = Column(String(250))

class Country(Base):
	__tablename__ = 'country'

	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		return {
			'name': self.name,
			'id': self.id,
		}

class Highlight(Base):
    __tablename__ = 'highlight'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(convert_unicode=True), nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship(Country)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

engine = create_engine('sqlite:///countries.db')
Base.metadata.create_all(engine)