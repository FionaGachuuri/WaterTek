from sqlalchemy import Column, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel, Base


class MeterReading(BaseModel, Base):
    """MeterReading table"""
    __tablename__ = "meter_readings"

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    reading_value = Column(Float, nullable=False)
    photo_url = Column(String(256), nullable=True)
    date = Column(DateTime, nullable=False)

    bill = relationship("Bill", backref="meter_readings", uselist=False)

    def __repr__(self):
        return f"<MeterReading value={self.reading_value} user_id={self.user_id} date={self.date}>"