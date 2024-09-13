#!/usr/bin/env python3
""" Authentication module """

import bcrypt
from db import DB
from user import User
from typing import Union
import uuid


class Auth:
    """ Auth class to manage authentication """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a new user """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except Exception:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate login credentials """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8'))
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ Create a new session ID for the user """
        user = self._db.find_user_by(email=email)
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ Get user by session_id """
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, session_id: str) -> None:
        """ Destroy a user session by clearing the session ID """
        user = self.get_user_from_session_id(session_id)
        if user:
            self._db.update_user(user.id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ Generate a reset password token """
        user = self._db.find_user_by(email=email)
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Update password using reset token """
        user = self._db.find_user_by(reset_token=reset_token)
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)


def _hash_password(password: str) -> str:
    """ Hash a password using bcrypt """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def _generate_uuid() -> str:
    """ Generate a new UUID """
    return str(uuid.uuid4())
