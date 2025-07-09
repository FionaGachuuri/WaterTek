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

    # Save the new reading first
    reading = MeterReading(
        user_id=user_id,
        reading_value=reading_value,
        date=reading_date or datetime.utcnow()
    )
    storage.new(reading)
    storage.save()

    # Now fetch the previous reading (excluding the one just added)
    previous_reading = (
        storage.session.query(MeterReading)
        .filter(
            MeterReading.user_id == user_id,
            MeterReading.id != reading.id
        )
        .order_by(MeterReading.date.desc())
        .first()
    )

    previous_value = previous_reading.reading_value if previous_reading else 0
    units_used = reading_value - previous_value
    amount_due = units_used * RATE_PER_UNIT

    bill = Bill(
        user_id=user_id,
        reading_id=reading.id,
        amount_due=amount_due,
        units_used=units_used,
        status="unpaid",
        date_due=datetime.utcnow()
    )
    storage.new(bill)
    storage.save()
    return bill.to_dict()