# app/services/billing.py
from app.models import storage
from app.models.user import User
from app.models.meter_reading import MeterReading
from app.models.bill import Bill
from datetime import datetime

RATE_PER_UNIT = 50

def generate_bill(user_id, reading_value, reading_date=None):
    """Create a bill based on the new meter reading."""
    user = storage.get(User, user_id)
    if not user:
        raise ValueError("User not found")

    # Get previous reading (if any)
    last_reading = (
        storage.session.query(MeterReading)
        .filter_by(user_id=user_id)
        .order_by(MeterReading.date.desc())
        .first()
    )

    previous_value = last_reading.reading_value if last_reading else 0
    units_used = reading_value - previous_value
    amount_due = units_used * RATE_PER_UNIT

    reading = MeterReading(
        user_id=user_id,
        reading_value=reading_value,
        date=reading_date or datetime.utcnow()
    )
    storage.new(reading)
    storage.save()

    bill = Bill(
        user_id=user_id,
        reading_id=reading.id,
        amount_due=amount_due,
        status="unpaid",
        date_due=datetime.utcnow()
    )
    storage.new(bill)
    storage.save()
    return bill.to_dict()