#!/usr/bin/python3
# models/base_model.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import uuid
from datetime import datetime

Base = declarative_base()


class BaseModel:
    id = Column(
        String(60),
        primary_key=True,
        nullable=False,
        unique=True,
        default=str(uuid.uuid4()),
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        if kwargs and "id" in kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ["created_at", "updated_at"]:
                        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, value)
        else:
            from models import storage

            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            if kwargs:
                for key, value in kwargs.items():
                    setattr(self, key, value)
            storage.new(self)

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        if not hasattr(self, "id"):
            raise AttributeError("'BaseModel' object has no attribute 'id'")

        from models import storage

        self.updated_at = datetime.utcnow()
        storage.save()

    def to_dict(self):
        obj_dict = self.__dict__.copy()
        if "_sa_instance_state" in obj_dict:
            del obj_dict["_sa_instance_state"]
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        return obj_dict

    def delete(self):
        from models import storage

        storage.delete(self)
        storage.save()
