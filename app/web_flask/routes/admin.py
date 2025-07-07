from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import storage
from app.models.user import User
from app.models.bill import Bill
from app.models.issue import Issue
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
    return render_template('admin/dashboard.html',
                           total_users=total_users,
                           total_bills=total_bills,
                           total_issues=total_issues)

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

def view_user_detail(user_id):
    user = storage.get(User, user_id)
    if not user:
        flash("User not found", "error")
        return redirect(url_for("admin.view_users"))
    
    bills = (
        storage.session.query(Bill)
        .filter_by(user_id=user_id)
        .order_by(Bill.date_due.desc())
        .all()
    )

    return render_template("admin/user_detail.html", user=user, bills=bills)

protected_user_detail = jwt_required()(admin_required(view_user_detail))
admin_bp.add_url_rule(
    '/users/<user_id>',
    view_func=protected_user_detail,
    endpoint='view_user_detail'
)

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
    """Admin view of all user-submitted issues."""
    issues = storage.session.query(Issue).all()
    return render_template('admin/issues.html', issues=issues)