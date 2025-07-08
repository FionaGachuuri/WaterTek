from flask import Blueprint, request, jsonify, redirect, url_for, render_template, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt, get_jwt_identity,
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies
)
from flask.views import MethodView
from app.models.user import User
from app import storage

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")


@auth_bp.route('/login', methods=['GET'])
def login_page():
    """Display login page."""
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET'])
def register_page():
    """Display registration page."""
    return render_template('register.html')


class RegisterUser(MethodView):
    """Register a new user with role (admin or user)."""
    def post(self):
        try:
            data = request.get_json()

            # print("Received data for registration:", data)
            if not data:
                return jsonify({"error": "No user data provided"}), 400

            required_fields = ["email", "phone", "password", "first_name", "last_name", "role"]
            if not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400

            # Validate role
            if data["role"] not in ["admin", "user"]:
                return jsonify({"error": "Role must be either 'admin' or 'user'"}), 400

            # Check if email already exists
            existing_email = storage.session.query(User).filter_by(email=data["email"]).first()
            if existing_email:
                return jsonify({"error": "Email already exists"}), 400

            # Check if phone number already exists
            existing_phone = storage.session.query(User).filter_by(phone=data["phone"]).first()
            if existing_phone:
                return jsonify({"error": "Phone number already exists"}), 400

            # print(f"generate_password_hash: {generate_password_hash}")

            hashed_password = generate_password_hash(data["password"])

            user = User(
                email=data["email"],
                phone=data["phone"],
                password_hash=hashed_password,
                first_name=data["first_name"],
                last_name=data["last_name"],
                role=data["role"]
            )

            # print(f"storage.new: {getattr(storage, 'new', None)}")
            # print(f"storage.save: {getattr(storage, 'save', None)}")

            storage.new(user)
            storage.save()

            return jsonify({"message": "User registered successfully"}), 201

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500


class LoginUser(MethodView):
    """Login an existing user and include role in JWT claims."""
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No credentials provided"}), 400

            email = data.get("email")
            password = data.get("password")
            if not email or not password:
                return jsonify({"error": "Email and password are required"}), 400

            user = storage.session.query(User).filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):
                token = create_access_token(
                    identity=user.id,
                    additional_claims={"role": user.role}
                )
                response = make_response(jsonify({"message": "Login successful"}))
                set_access_cookies(response, token)
                return response, 200

            else:
                return jsonify({"error": "Invalid email or password"}), 401

        except Exception as e:
            return jsonify({"error": str(e)}), 500


class LogoutUser(MethodView):
    """Logout handler for both GET and POST requests."""
    def get(self):
        """GET request - redirect to login page."""
        return redirect('/auth/login')
    
    @jwt_required()
    def post(self):
        """POST request - API logout (stateless)."""
        response = jsonify({"message": "Logout successful"})
        unset_jwt_cookies(response)
        return response, 200


class DeleteUser(MethodView):
    """Delete a user by ID (only allowed for admin)."""
    @jwt_required()
    def delete(self):
        try:
            user_id = get_jwt_identity()
            current_user = storage.get(User, user_id)
            if not current_user or not current_user.is_admin:
                return jsonify({"error": "Admins only can delete users"}), 403

            target_user_id = request.args.get("id")
            if not target_user_id:
                return jsonify({"error": "User ID is required"}), 400

            target_user = storage.get(User, target_user_id)
            if not target_user:
                return jsonify({"error": "User not found"}), 404

            storage.delete(target_user)
            storage.save()
            return jsonify({"message": "User deleted successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


# Register the views
auth_bp.add_url_rule("/register", view_func=RegisterUser.as_view("register"))
auth_bp.add_url_rule("/login", view_func=LoginUser.as_view("login"))
auth_bp.add_url_rule("/logout", view_func=LogoutUser.as_view("logout"))
auth_bp.add_url_rule("/user/delete", view_func=DeleteUser.as_view("delete_user"))
