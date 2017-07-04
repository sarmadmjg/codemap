#! /usr/bin/env python3

"""
    Model for the app database
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Category(Base):
    """Category table entry

    Attributes:
        description (str): short description
        long_name (str): name displayed in html
        name (str): unique name used in urls (no spaces)
    """
    __tablename__ = 'category'

    name = Column(String(80), primary_key=True)
    long_name = Column(String(80), nullable=False)
    description = Column(String(250))

    def serialize(self):
        """serialize the category

        Returns:
            dict: key/value representation of the category
        """
        return {
            'name': self.name,
            'long_name': self.long_name,
            'description': self.description,
            'entries_url': '/api/categories/{}/entries/'.format(self.name)
        }


class Entry(Base):
    """Entry table class

    Attributes:
        category (str): category name
        description (str): short description
        id (int): unique id
        link (str): link
        name (str): short name
        poster_uid (str): user id of the original poster
    """
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    link = Column(String, nullable=False)
    category = Column(String(80), ForeignKey('category.name'))
    poster_uid = Column(String, ForeignKey('user.uid'))

    def serialize(self):
        """serialize the category

        Returns:
            dict: key/value representation of the entry
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'link': self.link,
            'category': self.category,
            'poster_uid': self.poster_uid
        }


class User(Base):
    """User table class

    Attributes:
        email (str): email
        name (str): Full name
        uid (str): unique google uid
    """
    __tablename__ = 'user'

    uid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)


engine = create_engine('sqlite:///codemap.db')

Base.metadata.create_all(engine)
