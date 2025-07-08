from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import storage
from app.models.meter_reading import MeterReading
from app.models.bill import Bill
from app.models.user import User
from app.models.issue import Issue
from datetime import datetime
from app.services.billing import generate_bill

user_bp = Blueprint('user', __name__, url_prefix="/user")

@user_bp.route("/dashboard")
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)

    if not user:
        return render_template("errors/404.html"), 404
    
    # Get recent readings (last 10)
    recent_readings = (
        storage.session.query(MeterReading)
        .filter_by(user_id=user_id)
        .order_by(MeterReading.date.desc())
        .limit(10)
        .all()
    )

    # Get recent bills (last 10)
    recent_bills = (
        storage.session.query(Bill)
        .filter_by(user_id=user_id)
        .order_by(Bill.date_due.desc())
        .limit(10)
        .all()
    )
    
    return render_template("user/dashboard.html", 
                         recent_readings=recent_readings, 
                         recent_bills=recent_bills)

@user_bp.route("/submit-reading", methods=["GET", "POST"])
@jwt_required()
def submit_reading():
    if request.method == "GET":
        user_id = get_jwt_identity()
        # Get recent readings for display
        recent_readings = (
            storage.session.query(MeterReading)
            .filter_by(user_id=user_id)
            .order_by(MeterReading.date.desc())
            .limit(5)
            .all()
        )
        return render_template("user/submit_reading.html", recent_readings=recent_readings)
    
    # POST method
    user_id = get_jwt_identity()
    reading_value = request.form.get("reading")

    if not reading_value:
        flash("Reading value is required!", "error")
        return redirect(url_for("user.submit_reading"))
    
    try:
        reading_value = float(reading_value)
    except ValueError:
        flash("Reading must be a number!", "error")
        return redirect(url_for("user.submit_reading"))
    
    try:
        reading = MeterReading(
            user_id=user_id,
            reading_value=reading_value,
            date=datetime.utcnow()
        )
        storage.new(reading)
        storage.save()

        # Generate bill for this reading
        generate_bill(user_id, reading)

        flash("Meter reading submitted successfully.", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")

    return redirect(url_for("user.dashboard"))

@user_bp.route("/report-issue", methods=["GET", "POST"])
@jwt_required()
def report_issue():
    if request.method == "GET":
        user_id = get_jwt_identity()
        # Get recent issues for display
        recent_issues = (
            storage.session.query(Issue)
            .filter_by(user_id=user_id)
            .order_by(Issue.created_at.desc())
            .limit(3)
            .all()
        )
        return render_template("user/report_issue.html", recent_issues=recent_issues)
    
    # POST method
    user_id = get_jwt_identity()
    title = request.form.get("title")
    description = request.form.get("description")
    category = request.form.get("category", "other")
    priority = request.form.get("priority", "medium")

    if not title or not description:
        flash("Both title and description are required.", "error")
        return redirect(url_for("user.report_issue"))
    
    try:
        issue = Issue(
            user_id=user_id, 
            title=title, 
            description=description,
            status='open'
        )
        storage.new(issue)
        storage.save()
        flash("Issue submitted successfully.", "success")
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
    
    return redirect(url_for("user.dashboard"))