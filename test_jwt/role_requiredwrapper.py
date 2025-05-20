from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if identity.get("role") != required_role:
                return jsonify({"msg": "Access forbidden: insufficient role"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


@app.route("/admin", methods=["GET"])
@role_required("admin")
def admin_dashboard():
    return jsonify({"msg": "Welcome to the admin dashboard!"})