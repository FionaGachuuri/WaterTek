from sqlalchemy import Column, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel, Base


class Bill(BaseModel, Base):
    """Billing class represssenting billing data"""
    __tablename__ = "bills"

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    reading_id = Column(String(60), ForeignKey('meter_readings.id'), nullable=False)

    amount_due = Column(Float, nullable=False)
    units_used = Column(Float, nullable=False)
    status = Column(String(6), nullable=False, default="unpaid")
    date_due = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Bill amount_due={self.amount_due} user_id={self.user_id}"