#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_type
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage
import os


class State(BaseModel, Base):
    """ State class / table model"""
    __tablename__ = 'states'
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete, delete-orphan')
    else:
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            @property
            def cities(self):
                """إرجاع قائمة المدن مرتبطة بالولاية"""
                cities_list = []
                for city in storage.all(City).values():
                    if city.state_id == self.id:
                        cities_list.append(city)
                return cities_list