"""
Init file for routes module
"""
from flask import Blueprint, redirect, url_for
from flask_jwt_extended import get_jwt_identity
from app.models import storage
from app.models.user import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main index route that redirects to appropriate dashboard."""
    try:
        user_id = get_jwt_identity()
        if user_id:
            user = storage.get(User, user_id)
            if user and user.is_admin:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('user.dashboard'))
    except:
        pass
    
    # If not authenticated, redirect to login
    return redirect(url_for('auth.login_page'))