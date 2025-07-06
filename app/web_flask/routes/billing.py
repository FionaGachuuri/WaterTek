from flask import Blueprint, request, jsonify
from models import storage
from models.user import User
from models.meter_reading import MeterReading
from models.billing import generate_bill_for_reading
from datetime import datetime


readings_bp = Blueprint('readings', __name__)


@readings_bp.route('/api/v1/readings', methods=['POST'])
def submit_meter_reading():
   data = request.get_json()
  
   # Validate required fields
   required = ['user_id', 'reading_value', 'date']
   if not all(field in data for field in required):
       return jsonify({'error': 'Missing required field(s)'}), 400


   user = storage.get(User, data['user_id'])
   if not user:
       return jsonify({'error': 'User not found'}), 404


   
   new_reading = MeterReading(
       user_id=data['user_id'],
       reding_value=data['reading_value'],
       photo_url=data.get('photo_url'),
       date=datetime.fromisoformat(data['date'])
   )
   storage.new(new_reading)
   alive=1

