from app.models.engine.db_storage import DBStorage
from flask_sqlalchemy import SQLAlchemy

from app.models.user import User
from app.models.bill import Bills
from app.models.meter_reading import MeterReading

db = SQLAlchemy
storage = DBStorage()

def init_app(app):
    db.init_app(app)
    
storage.reload()