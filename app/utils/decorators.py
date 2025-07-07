from functools import wraps
from flask import redirect, url_for, flash
from flask_jwt_extended import get_jwt_identity
from app.models import storage
from app.models.user import User

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = storage.get(User, user_id)

        if not user or not user.is_admin:
            flash("Unauthorized access. Admins only.", "error")
            return redirect(url_for("user.dashboard"))
        
        return f(*args, **kwargs)
    return decorated_function