#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from sys import argv
import os
from os import getenv
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import MySQLdb

classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
          }


class DBStorage:
    """DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage"""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.
            format(user, password, host, database),
            pool_pre_ping=True)
        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """querry current database session"""
        self.__session = Session(bind=self.__engine)
        query_data = []
        if cls:
            query_data.append(self.__session.query(cls).all())
        else:
            query_data.append(self.__session.query(User).all())
            query_data.append(self.__session.query(State).all())
            query_data.append(self.__session.query(City).all())
            query_data.append(self.__session.query(Amenity).all())
            query_data.append(self.__session.query(Place).all())
            query_data.append(self.__session.query(Review).all())

        dict_objs = {}
        for row in query_data:
            for i in range(len(row)):
                dict_objs["{}.{}".format(
                    type(row[i]).__name__, row[i].id)] = row[i]
        return dict_objs

    def new(self, obj):
        """ add obj to curr db """

        if obj:
            self.__session.add(obj)

    def save(self):
        """ save changes to database """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete given obj """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ reload """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False
            ))
        self.__session = Session()

    def close(self):
        """closes session"""
        self.__session.close()
