# models/state.py
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage_type


class State(BaseModel, Base):
    __tablename__ = "states"
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all, delete")
    else :
        name = ''