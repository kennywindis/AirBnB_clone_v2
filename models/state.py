#!/usr/bin/python3
"""This is the state class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
import os
from models.city import City
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = 'states'
    if (os.getenv('HBNB_TYPE_STORAGE') != 'db'):
        name = ''

        @property
        def cities(self):
            """
            Info
            """
            new_list = []
            all_entries = models.storage.all(City)
            for key, value in all_entries.items():
                if self.id == value.state_id:
                    new_list.append(value)

            return new_list
    else:
        name = Column("name", String(128), nullable=False)
        cities = relationship("City", cascade='all, delete', backref='state')
