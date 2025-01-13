from flask import Blueprint, request, jsonify

from ..config.responses import INVALID_INPUT_RESPONSE
from .auth_service import AuthService
from ..utils.is_data_full import is_data_full

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user with a hashed password.

    **Method:** `POST`

    **Request Body:**
    json
    {
      "username": "testuser",
      "password": "password123"
    }

    **Response:**
    - `201 Created`
    json
    {
      "message": "User registered successfully"
    }

    - `400 Bad Request`
    json
    {
      "error": "Invalid input"
    }
    """
    data = request.json
    if not is_data_full(data, "username", "password"):
        response, status = INVALID_INPUT_RESPONSE
        return jsonify(response), status

    response, status = AuthService.register_user(data["username"], data["password"])
    return jsonify(response), status


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
      "error": "Invalid credentials"
    }

    - `400 Bad Request`
    json
    {
      "error": "Invalid input"
    }
    """
    data = request.json
    if not is_data_full(data, "username", "password"):
        response, status = INVALID_INPUT_RESPONSE
        return jsonify(response), status

    response, status = AuthService.authenticate_user(data["username"], data["password"])
    return jsonify(response), status
