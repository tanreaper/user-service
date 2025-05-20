from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

app = Flask(__name__)
app.con
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # use env var in real apps
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

# Dummy users for now
users = {
    "testuser": {
        "password": "password123"
    }
}

# @app.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     username = data.get("username")
#     password = data.get("password")

#     user = users.get(username)
#     if not user or user["password"] != password:
#         return jsonify({"msg": "Bad username or password"}), 401

#     access_token = create_access_token(identity=username)
#     return jsonify(access_token=access_token)


@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({
        "msg": f"Welcome, {current_user}!"
    })

from both header and cookies
from flask import make_response

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)
    if not user or user["password"] != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)

    user_agent = request.headers.get("User-Agent", "").lower()
    if "postman" in user_agent:
        # For Postman → return in JSON
        return jsonify(access_token=access_token)
    else:
        # For browser → set as cookie
        resp = jsonify({"msg": "Login successful"})
        from flask_jwt_extended import set_access_cookies
        set_access_cookies(resp, access_token)
        return resp


if __name__ == "__main__":
    app.run(debug=True)