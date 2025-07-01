from sqlalchemy import Column, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel, Base


class MeterReading(BaseModel, Base):
    """MeterReading table"""
    __tablename__ = "Meterreadings"

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    reding_value = Column(Float, nullable=False)
    photo_url = Column(String(256), nullable=True)
    date = Column(DateTime, nullable=False)

    bill = relationship("Bill", backref="Meterreadings", uselist=False)