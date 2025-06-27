from datetime import datetime
from os import getenv
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models
import uuid

time_format = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base()


class BaseModel:
    """The base class for all classes"""
    id = Column(String(60), primary_key=True, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize the BaseModel"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

        # Convert string dates back to datetime
        if "created_at" in kwargs and isinstance(self.created_at, str):
            self.created_at = datetime.strptime(kwargs["created_at"], time_format)
        else:
            self.created_at = datetime.utcnow()

        if "updated_at" in kwargs and isinstance(self.updated_at, str):
            self.updated_at = datetime.strptime(kwargs["updated_at"], time_format)
        else:
            self.updated_at = datetime.utcnow()

        if "id" not in kwargs:
            self.id = str(uuid.uuid4())

    def save(self):
        """Update 'updated_at' with current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self)
        """Convert instance into key/values dictionary format"""
        new_dict = self.__dict__.copy()

        # conver datetime attribute to string format
        if "created_at" in new_dict:
            new_dict["created_at"] = self.created_at.isoformat()
        if "updated_at" in new_dict:
            new_dict["updated_at"] = self.created_at.isoformat()
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        return new_dict
    
    def __str__(self):
        """String representation of BaseModel class"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
    
    def delete(self):
        """Delete the current instance from storage"""
        models.storage.delete(self)