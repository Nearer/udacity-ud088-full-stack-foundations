from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date, Text, Table
from sqlalchemy import create_engine, func, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

adopters_puppies = Table(
        'adopters_puppies', Base.metadata,
        Column('adopter_id', ForeignKey('adopters.id'), primary_key=True),
        Column('puppy_id', ForeignKey('puppies.id'), primary_key=True)
)


class Adopter(Base):
    __tablename__ = 'adopters'
    id = Column(
            Integer,
            primary_key=True
    )
    name = Column(
            String(100),
            nullable=False
    )
    puppies = relationship('Puppy', secondary=adopters_puppies, back_populates='adopters')

    def __repr__(self):
        return '<Adopter(id={}, name={})>'.format(
                self.id, self.name
        )


class Profile(Base):
    __tablename__ = 'profiles'
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
    puppy = relationship('Puppy', back_populates='profile', uselist=False)


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
            ForeignKey('shelters.id')
    )

    shelter = relationship('Shelter', back_populates='puppies')
    profile_id = Column(
            Integer,
            ForeignKey('profiles.id')
    )
    profile = relationship('Profile', uselist=False, back_populates='puppy',
                           cascade='all, delete')
    adopters = relationship('Adopter', secondary='adopters_puppies', back_populates='puppies')

    def __repr__(self):
        return '<Puppy(id={}, name={}, gender={}, weight={})>'.format(
                self.id, self.name, self.gender, self.weight
        )


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
    puppies = relationship('Puppy', back_populates='shelter')
    maximum_capacity = Column(
            Integer,
            nullable=False
    )
    current_occupancy = column_property(select([func.count(Puppy.id)])
                                        .where(Puppy.shelter_id == id)
                                        .correlate_except(Puppy))

    def __repr__(self):
        return '<Shelter(id={}, name={}, city={}, current_occupancy={}, maximum_capacity={})>' \
            .format(
                self.id, self.name, self.city, self.current_occupancy, self.maximum_capacity
        )


name = 'puppies'  # db name goes here

engine = create_engine('sqlite:///{}.db'.format(name))
Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
