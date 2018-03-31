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
    email = Column(String(250), nullable=False, unique=True)
    picture = Column(String(250))


class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
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
    prologue = Column(String(convert_unicode=True), nullable=False)
    description = Column(String(convert_unicode=True), nullable=False)
    img_url = Column(String(convert_unicode=True), nullable=True)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship(Country)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'prologue': self.prologue,
            'description': self.description,
            'img_url': self.img_url,
        }


engine = create_engine('sqlite:///countries.db')
Base.metadata.create_all(engine)
