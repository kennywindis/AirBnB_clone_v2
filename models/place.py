#!/usr/bin/python3
"""Define the class Place."""
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv
from models import storage
# from models.amenity import Amenity


metadata = Base.metadata
place_amenity = Table('place_amenity', metadata,
                      Column(
                          'place_id',
                          String(60),
                          ForeignKey('places.id'),
                          primary_key=True,
                          nullable=False),
                      Column(
                          'amenity_id',
                          String(60),
                          ForeignKey('amenities.id'),
                          primary_key=True,
                          nullable=False))


class Place(BaseModel, Base):
    """Define the class Place that inherits from BaseModel."""
    __tablename__ = 'places'
    if getenv('HBNB_TYPE_STORAGE') == 'db':

        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = []
        amenities = relationship(
            'Amenity',
            secondary=place_amenity,
            back_populates='place_amenities',
            viewonly=False)

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def amenities(self):
            from models.amenity import Amenity
            d = storage.all(Amenity)
            instances = []
            for v in d.values():
                instances.append(v)
            return instances
