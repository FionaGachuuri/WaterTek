from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import storage

admin_bp = Blueprint('admin', __name__, url_prefix="/api/admin")

class UserList(MethodView):
    """Admin: List and create users."""

    @jwt_required()
    def get(self):
        """List all users."""
        users = storage.session.query(User).all()
        data = [u.to_dict() for u in users]
        return jsonify(data), 200

    @jwt_required()
    def post(self):
        """Admin can create a user directly."""
        data = request.get_json()
        required_fields = ["email", "phone", "password", "first_name", "last_name"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Check if user already exists
        existing = storage.session.query(User).filter_by(email=data["email"]).first()
        if existing:
            return jsonify({"error": "Email already exists"}), 400

        hashed_password = generate_password_hash(data["password"])
        user = User(
            email=data["email"],
            phone=data["phone"],
            password_hash=hashed_password,
            first_name=data["first_name"],
            last_name=data["last_name"],
            role=data.get("role", "user")
        )
        storage.new(user)
        storage.save()
        return jsonify({"message": "User created successfully", "user": user.to_dict()}), 201


class UserDetail(MethodView):
    """Admin: Get, update, or delete a single user."""

    @jwt_required()
    def get(self, user_id):
        user = storage.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_dict()), 200

    @jwt_required()
    def put(self, user_id):
        data = request.get_json()
        user = storage.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        for field in ["email", "phone", "first_name", "last_name", "role"]:
            if field in data:
                setattr(user, field, data[field])
        storage.save()
        return jsonify({"message": "User updated", "user": user.to_dict()}), 200

    @jwt_required()
    def delete(self, user_id):
        user = storage.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        storage.delete(user)
        storage.save()
        return jsonify({"message": "User deleted"}), 200


# Register the routes
admin_bp.add_url_rule('/users', view_func=UserList.as_view('users'))
admin_bp.add_url_rule('/users/<user_id>', view_func=UserDetail.as_view('user_detail'))
