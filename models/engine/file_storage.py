#!/usr/bin/python3
# models/engine/file_storage.py

"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""

    __file_path = "file.json"
    __objects = {}

    def all(self, classes=None):
        """Returns a dictionary of models currently in storage"""
        if not classes is None:
            cls_name = classes.__name__
            data = {}
            for key in self.__objects.keys():
                if key.split(".")[0] == cls_name:
                    data[key] = self.__objects[key]
            return data
        else:
            return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.all()[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        temp = {key: value.to_dict() for key, value in self.all().items()}
        with open(FileStorage.__file_path, "w") as file:
            json.dump(temp, file)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
        }
        try:
            with open(FileStorage.__file_path, "r") as file:
                temp = json.load(file)
                for key, val in temp.items():
                    if val["__class__"] in classes:
                        self.all()[key] = classes[val["__class__"]](**val)
                    else:
                        print("NOT FOUND IN CLASSES")
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """deletes the object obj from the attribute
        __objects if it's inside it
        """
        if obj is None:
            return
        obj_key = obj.to_dict()["__class__"] + "." + obj.id
        if obj_key in self.__objects.keys():
            del self.__objects[obj_key]
