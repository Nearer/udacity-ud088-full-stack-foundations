from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text
from sqlalchemy.types import Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
name = 'puppies'  # db name goes here


class Shelter(Base):
    __tablename__ = 'shelter'
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
    zipCode = Column(
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


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(
            Integer,
            primary_key=True
    )
    picture = Column(
            String(250),
            nullable=True
    )
    description = Column(
            Text,
            nullable=True
    )
    specialNeeds = Column(
            Text,
            nullable=True
    )


class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(
            Integer,
            primary_key=True
    )
    name = Column(
            String(100),
            nullable=False
    )
    dateOfBirth = Column(
            Date,
            nullable=True
    )
    gender = Column(
            String(6),
            nullable=False
    )
    weight = Column(
            Float,
            nullable=False
    )
    shelter_id = Column(
            Integer,
            ForeignKey('shelter.id')
    )
    shelter = relationship(Shelter)
    profile_id = Column(
            Integer,
            ForeignKey(Profile.id)
    )
    profile = relationship(Profile, uselist=False, backref='puppy')


engine = create_engine('sqlite:///{}.db'.format(name))
Base.metadata.create_all(engine)
