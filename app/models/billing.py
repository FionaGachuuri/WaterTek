from datetime import timedelta
from sqlalchemy import extract
from models.bill import Bill
from models.meter_reading import MeterReading
from models import storage


def generate_bill_for_reading(user, current_reading):
    """billing function"""
    
   unit_price = 110
   
   previous_reading = (
       session.query(MeterReading)
       .filter(MeterReading.user_id == user.id,
               MeterReading.date < current_reading.date)
       .order_by(MeterReading.date.desc())
       .first()
   )


   if not previous_reading:
       return


   current_month = current_reading.date.month
   current_year = current_reading.date.year
   previous_month = previous_reading.date.month
   previous_year = previous_reading.date.year


   if current_month == previous_month and current_year == previous_year:
       return  


   
   units_used = current_reading.reading_value - previous_reading.reading_value
   if units_used < 0:
       return 


   amount_due = units_used * unit_price 


   bill = Bill(
       user_id=user.id,
       reading_id=current_reading.id,
       units_used=units_used,
       amount_due=amount_due,
       status="unpaid",
       date_due=current_reading.date + timedelta(days=14)
   )

   storage.new()
   storage.add(bill)
   storage.save()
