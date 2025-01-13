from flask import Response

from app.config.responses import (
    INVALID_CREDENTIALS_RESPONSE,
    REGISTERED_SUCCESSFULLY_RESPONSE,
    USER_ALREADY_EXISTS_RESPONSE,
    acces_token_response,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models import User
from app.config.db import db


class AuthService:
    @staticmethod
    def register_user(username: str, password: str) -> tuple[Response, int]:
        """
        New User Registration.
        """
        if User.query.filter_by(username=username).first():
            return USER_ALREADY_EXISTS_RESPONSE

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return REGISTERED_SUCCESSFULLY_RESPONSE

    @staticmethod
    def authenticate_user(username: str, password: str) -> tuple[Response, int]:
        """
        User authentication and issuance of JWT token.
        """
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=str(user.id))
            return acces_token_response(access_token)
        return INVALID_CREDENTIALS_RESPONSE
