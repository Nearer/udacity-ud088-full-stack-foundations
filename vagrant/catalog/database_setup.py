import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.types import Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
name = 'puppies'  # db name goes here


class Shelter(Base):
    __tablename__ = 'shelters'
    name = Column(
            String(100),
            nullable=False
    )
    address = Column(
            String(200),
            nullable=False
    )
    city = Column(
            String(200),
            nullable=False
    )
    state = Column(
            String(100),
            nullable=False
    )
    zip_code = Column(
            Integer,
            nullable=False
    )
    website = Column(
            String(500),
            nullable=True
    )
    id = Column(
            Integer,
            primary_key=True
    )


class Puppy(Base):
    __tablename__ = 'puppies'
    id = Column(
            Integer,
            primary_key=True
    )
    name = Column(
            String(100),
            nullable=False
    )
    date_of_birth = Column(
            Date,
            nullable=True
    )
    gender = Column(
            String(6),
            nullable=False
    )
    weight = Column(
            Numeric(10),
            nullable=False
    )
    shelter_id = Column(
            Integer,
            ForeignKey('shelters.id')
    )
    shelter = relationship(Shelter)

engine = create_engine('sqlite:///{}.db'.format(name))
Base.metadata.create_all(engine)
