from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(
        String(80),
        nullable=False
    )
    id = Column(
        Integer,
        primary_key=True
    )
    menu_items = relationship('MenuItem', back_populates='restaurant')

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }

class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(
        String(80),
        nullable=False
    )
    id = Column(
        Integer,
        primary_key=True
    )
    course = Column(
        String(250)
    )
    description = Column(
        Text
    )
    price = Column(
        Float
    )
    restaurant_id = Column(
        Integer,
        ForeignKey('restaurant.id')
    )
    restaurant = relationship('Restaurant', back_populates='menu_items')

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': '${:,.2f}'.format(self.price),
            'course': self.course
        }


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
