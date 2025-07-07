from flask import Blueprint, request, jsonify
from app.services.billing import generate_bill
from datetime import datetime

billing_bp = Blueprint('billing', __name__, url_prefix="/billing")

@billing_bp.route('/submit-reading', methods=['POST'])
def submit_meter_reading():
    data = request.get_json()

    required = ['user_id', 'reading_value']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required field(s)'}), 400

    try:
        reading_value = float(data['reading_value'])
        reading_date = datetime.fromisoformat(data['date']) if 'date' in data else None

        bill_data = generate_bill(
            user_id=data['user_id'],
            reading_value=reading_value,
            reading_date=reading_date
        )

        return jsonify({
            'message': 'Meter reading and bill created successfully',
            'bill': bill_data
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Internal error: {str(e)}'}), 500
