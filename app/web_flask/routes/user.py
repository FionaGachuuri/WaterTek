from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import storage
from app.models.meter_reading import MeterReading
from app.models.bill import Bill
from app.models.user import User
from datetime import datetime
from app.billing import generate_bill 

user_bp = Blueprint('user', __name__, url_prefix="/user")

@user_bp.route("/dashboard")
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)

    if not user:
        return render_template("errors/404.html"), 404
    
    readings = (
        storage.session.query(MeterReading)
        .filter_by(user_id=user_id)
        .order_by(MeterReading.date.desc())
        .all()
    )

    bills = []
    for reading in readings:
        if reading.bill:
            bills.append({
                "date": reading.date.strftime("%Y-%m-%d"),
                "reading": reading.reading_value,
                "amount": reading.bill.amount_due,
                "status": reading.bill.status
            })
    
    return render_template("user/dashboard.html", user=user, bills=bills)

@user_bp.route("/submit-reading", methods=["POST"])
@jwt_required()
def submit_reading():
    user_id = get_jwt_identity()
    reading_value = request.form.get("reading")

    if not reading_value:
        flash("Reading value is required!", "error")
        return redirect(url_for("user.dashboard"))
    
    try:
        reading_value = float(reading_value)
    except ValueError:
        flash("Reading must be a number!", "error")
        return redirect(url_for("user.dashboard"))
    
    
    try:
        reading = MeterReading(
            user_id=user_id,
            reading_value=reading_value,
            date=datetime.utcnow()
        )
        storage.new(reading)
        storage.save()

        generate_bill(user_id, reading)

        flash("Meter reading submitted successfully.", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")

    return redirect(url_for("user.dashboard"))

@user_bp.route("/submit-issue", methods=["POST"])
@jwt_required()
def submit_issue():
    user_id = get_jwt_identity()
    title = request.form.get("title")
    description = request.form.get("description")

    if not title or not description:
        flash("Both title and description required.", "error")
        return redirect(url_for("user.dashboard"))
    
    try:
        from app.models.issue import Issue
        issue = Issue(user_id=user_id, title=title, description=description)
        storage.new(issue)
        storage.save()
        flash("Issue submited successfully.", "success")
    except Exception as e:
        flash(f"An error occured: {str(e)}", "error")
    
    return redirect(url_for("user.dashboard"))


        