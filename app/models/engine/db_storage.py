import os
import pymysql
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.models.base_model import BaseModel, Base
from app.models.user import User
from app.models.bill import Bill
from app.models.meter_reading import MeterReading

pymysql.install_as_MySQLdb()
load_dotenv()


classes = {
    "User": User,
    "Bill": Bill,
    "MeterReading": MeterReading
}

class DBStorage:
    """Handle database interactions using SQLAlchemy for MySQL"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize db connections using env variables"""
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")

        self.__engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
            pool_pre_ping=True,
            connect_args={
                "ssl": {
                    "ca": os.getenv("DB_SSL_CA")
                }
            }
        )

        if os.getenv("WATERTEK_ENV") == "test":
            Base.metadata.drop_all(self.__engine)
        
        self.reload()
        

    def reload(self):
        """Create session and bind it to the engine."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def new(self, obj):
        """Adds new object to session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from session"""
        if obj:
            self.__session.delete(obj)
            self.save()

    def all(self, cls=None):
        """Retrieve all objects from the database"""
        obj_dict = {}
        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = f"{obj.__class__.__name__}.{obj.id}"
                obj_dict[key] = obj
        else:
            for model in classes.values():
                objs = self.__session.query(model).all()
                for obj in objs:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    obj_dict[key] = obj
        return obj_dict

    def get(self, cls, id):
        """Retrieve an obj by class and ID."""
        if cls not in classes.values() or id is None:
            return None
        try:
            return self.__session.query(cls).get(id)
        except Exception:
            return None

    def close(self):
        """Close the session"""
        self.__session.remove()

    @property
    def session(self):
        """Expose the session"""
        return self.__session()