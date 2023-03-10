#!/usr/bin/python3
from models.base_model import BaseModel, Base
from models.place import place_amenity
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class Amenity(BaseModel, Base):
    """class Amenity"""
    __tablename__ = 'amenities'
    if os.getenv("HBNB_TYPE_STORAGE") == "db":

        name = Column(String(128), nullable=False)
        place_amenities = relationship(
            'Place',
            secondary='place_amenity',
            back_populates='amenities')

    else:

        name = ""
