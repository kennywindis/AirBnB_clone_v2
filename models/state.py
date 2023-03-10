#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel
from sqlalchemy import Column, String
from models.base_model import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.city import City
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship(
            'City',
            cascade="all,delete-orphan",
            backref="state")
    else:
        name = ""

        @property
        def cities(self):
            """cities"""
            cityArray = []
            for item in models.storage.all(City).values():
                if item.state_id == self.id:
                    cityArray.append(item)
            return cityArray
