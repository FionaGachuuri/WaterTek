from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """User class for WaterTek system"""
    __tablename__ = 'users'

    email = Column(String(128), nullable=False, unique=True)
    phone = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    location = Column(String(250), nullable=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    role = Column(String(20), nullable=False, default='user')

    # Relationship
    bill = relationship('Bills', backref="user", cascade="all, delete")
    reading = relationship("Meterreadings", backref="user", cascade="all, delete")