from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250), nullable=True)


class Entry(Base):
    __tablename__ = 'entry'

    category = relationship(Category)

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String, nullable=True)
    link = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))


engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
