from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    # name is used in links, no spaces
    name = Column(String(80), primary_key=True)
    # long_name is rendered in html
    long_name = Column(String(80), nullable=False)
    description = Column(String(250), nullable=True)

    def serialize(self):
        return {
            'name': self.name,
            'long_name': self.long_name,
            'description': self.description,
            'entries_url': '/api/categories/{}/entries/'.format(self.name)
        }


class Entry(Base):
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    link = Column(String, nullable=False)
    category = Column(String(80), ForeignKey('category.name'))
    poster_uid = Column(String, ForeignKey('user.uid'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'link': self.link,
            'category': self.category,
            'poster_uid': self.poster_uid
        }


class User(Base):
    __tablename__ = 'user'

    uid = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)


engine = create_engine('sqlite:///codemap.db')

Base.metadata.create_all(engine)
