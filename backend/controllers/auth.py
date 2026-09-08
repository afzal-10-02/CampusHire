from flask import Blueprint, request, jsonify
from database.models import Student, Admin, Company
from database.database import db
from werkzeug.security import check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, verify_jwt_in_request, get_jwt
from functools import wraps

auth = Blueprint('auth', __name__)



@auth.route("/login", methods = ["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")


    # 1. Validate incoming payload
    if not email or not password or not role:
        return jsonify({"status": "error", "message": "Email, Password, and Role are Required."}), 400
    
    user = None

    # 2. Query the correct table based on client request
    if role == "student":
        user = Student.query.filter_by(email=email).first()
    elif role == "admin":
        user = Admin.query.filter_by(email=email).first()
    elif role == "company":
        user = Company.query.filter_by(email=email).first()

    else:
        return jsonify({"status": "error", "message": "Invalid role specified."}), 400
    

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.email, additional_claims={"role": role})

        if role == "student":
            name = user.full_name
        elif role == "company":
            name = user.name
        else:
            name = "Admin"

        return jsonify({
            "status": "success", 
            "message": "Successfully logged in.", 
            "access_token": access_token, 
            "role": role,
            "name" : name
        }), 200
    
    # 4. Standardized error for bad password or user not found across all roles
    return jsonify({"status": "error", "message": "Invalid email or password."}), 401



def roles_required(*allowed_roles):
    """Decorator to restrict route access based on JWT claims."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 1. Force Flask to validate the Postman Bearer token header immediately
            verify_jwt_in_request()

            # 2. Now it is perfectly safe to pull out the claims dictionary
            claims = get_jwt()

            # 3. Extract the role from your token payload
            user_role = claims.get("role")
            print(f"User role from token: {user_role}")

            # 4. Enforce permissions
            if user_role not in allowed_roles:
                return jsonify({
                    "status": "error",
                    "message": "Forbidden: You do not have permission to access this resource.",
                }), 403

            return f(*args, **kwargs)

        return decorated_function
    return decorator


