from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import storage
from app.models.user import User
from app.models.bill import Bill
from app.models.issue import Issue
from app.models.meter_reading import MeterReading
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@jwt_required()
@admin_required
def dashboard():
    """Admin dashboard overview."""
    total_users = storage.session.query(User).count()
    total_bills = storage.session.query(Bill).count()
    total_issues = storage.session.query(Issue).count()
    unpaid_bills = storage.session.query(Bill).filter_by(status='unpaid').count()
    
    # Get recent issues (last 5)
    recent_issues = (
        storage.session.query(Issue)
        .join(User, Issue.user_id == User.id)
        .order_by(Issue.created_at.desc())
        .limit(5)
        .all()
    )
    
    # Get recent bills (last 5)
    recent_bills = (
        storage.session.query(Bill)
        .join(User, Bill.user_id == User.id)
        .order_by(Bill.date_due.desc())
        .limit(5)
        .all()
    )
    
    return render_template('admin/dashboard.html',
                           total_users=total_users,
                           total_bills=total_bills,
                           total_issues=total_issues,
                           unpaid_bills=unpaid_bills,
                           recent_issues=recent_issues,
                           recent_bills=recent_bills)

@admin_bp.route('/users')
@jwt_required()
@admin_required
def view_users():
    """Admin view of all users with pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = 10

    total_user = storage.session.query(User).count()
    users = (
        storage.session.query(User)
        .order_by(User.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return render_template(
        'admin/users.html',
        users=users,
        page=page,
        per_page=per_page,
        total_user=total_user
    )

@admin_bp.route('/users/<user_id>')
@jwt_required()
@admin_required
def view_user_detail(user_id):
    """Admin view of individual user details."""
    user = storage.get(User, user_id)
    if not user:
        flash("User not found", "error")
        return redirect(url_for("admin.view_users"))
    
    # Get user's bills
    bills = (
        storage.session.query(Bill)
        .filter_by(user_id=user_id)
        .order_by(Bill.date_due.desc())
        .all()
    )

    # Get user's recent meter readings
    recent_readings = (
        storage.session.query(MeterReading)
        .filter_by(user_id=user_id)
        .order_by(MeterReading.date.desc())
        .limit(10)
        .all()
    )

    return render_template("admin/user_detail.html", 
                         user=user, 
                         bills=bills,
                         recent_readings=recent_readings)

@admin_bp.route('/bills')
@jwt_required()
@admin_required
def view_bills():
    """Admin view of all bills with pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = 10

    total_bills = storage.session.query(Bill).count()
    bills = (
        storage.session.query(Bill)
        .join(User, Bill.user_id == User.id)
        .order_by(Bill.date_due.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return render_template(
        'admin/bills.html',
        bills=bills,
        page=page,
        per_page=per_page,
        total_bills=total_bills
    )

@admin_bp.route('/issues')
@jwt_required()
@admin_required
def view_issues():
    """Admin view of all user-submitted issues with pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = 10

    total_issues = storage.session.query(Issue).count()
    issues = (
        storage.session.query(Issue)
        .join(User, Issue.user_id == User.id)
        .order_by(Issue.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return render_template('admin/issues.html', 
                         issues=issues,
                         page=page,
                         per_page=per_page,
                         total_issues=total_issues)

@admin_bp.route('/bills/<bill_id>/mark-paid', methods=['POST'])
@jwt_required()
@admin_required
def mark_bill_paid(bill_id):
    """Mark a bill as paid."""
    bill = storage.get(Bill, bill_id)
    if not bill:
        flash("Bill not found", "error")
        return redirect(url_for("admin.view_bills"))
    
    try:
        bill.status = 'paid'
        storage.save()
        flash("Bill marked as paid successfully.", "success")
    except Exception as e:
        flash(f"Error updating bill: {str(e)}", "error")
    
    return redirect(url_for("admin.view_bills"))

@admin_bp.route('/issues/<issue_id>/update-status', methods=['POST'])
@jwt_required()
@admin_required
def update_issue_status(issue_id):
    """Update issue status."""
    issue = storage.get(Issue, issue_id)
    if not issue:
        flash("Issue not found", "error")
        return redirect(url_for("admin.view_issues"))
    
    new_status = request.form.get('status')
    if new_status not in ['open', 'in_progress', 'resolved']:
        flash("Invalid status", "error")
        return redirect(url_for("admin.view_issues"))
    
    try:
        issue.status = new_status
        storage.save()
        flash(f"Issue status updated to {new_status}.", "success")
    except Exception as e:
        flash(f"Error updating issue: {str(e)}", "error")
    
    return redirect(url_for("admin.view_issues"))