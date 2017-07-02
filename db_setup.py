from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    # name will appear in links (no spaces), long_name is rendered in the page
    name = Column(String(80), nullable=False)
    long_name = Column(String(80), nullable=False)
    description = Column(String(250), nullable=True)


class Entry(Base):
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    link = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))


engine = create_engine('sqlite:///codemap.db')

Base.metadata.create_all(engine)
