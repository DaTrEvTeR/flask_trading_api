from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from ..config.db import db
from ..models import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user with a hashed password.

    **Method:** `POST`

    **Request Body:**
    ```json
    {
      "username": "testuser",
      "password": "password123"
    }
    ```

    **Response:**
    - `201 Created`
    ```json
    {
      "message": "User registered successfully"
    }
    ```
    """
    data = request.json
    hashed_password = generate_password_hash(data["password"])
    new_user = User(username=data["username"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Logs in a user and returns a JWT token upon successful authentication.

    **Method:** `POST`

    **Request Body:**
    json
    {
      "username": "testuser",
      "password": "password123"
    }

    **Response:**
    - `200 OK`
    json
    {
      "access_token": "<JWT-TOKEN>"
    }

    - `401 Unauthorized`
    json
    {
      "message": "Invalid credentials"
    }
    """
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid credentials"}), 401
