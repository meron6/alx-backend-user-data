#!/usr/bin/env python3
"""
Auth module for user authentication service.
"""
import bcrypt
from uuid import uuid4
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        Returns a salted, hashed password, using bcrypt.
        Args:
            password (str): the password to hash
        Returns:
            bytes: the hashed password
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def _generate_uuid(self) -> str:
        """
        Generates a new UUID.
        Returns:
            str: UUID as string
        """
        return str(uuid4())

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user if the email is not already in the database.
        Args:
            email (str): email of the user
            password (str): user's password
        Returns:
            User: the registered User object
        Raises:
            ValueError: if user with email already exists
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login credentials.
        Args:
            email (str): user's email
            password (str): user's password
        Returns:
            bool: True if login is successful, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Creates a new session for a user identified by email.
        Args:
            email (str): user's email
        Returns:
            str: the session ID, or None if user not found
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Finds a user by session ID.
        Args:
            session_id (str): the session ID
        Returns:
            User: the User object, or None if no user is found
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a user's session.
        Args:
            user_id (int): the user's ID
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token for a user identified by email.
        Args:
            email (str): the user's email
        Returns:
            str: reset token
        Raises:
            ValueError: if the user is not found
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError("User not found")

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password using a reset token.
        Args:
            reset_token (str): the reset token
            password (str): the new password
        Raises:
            ValueError: if the reset token is invalid
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = self._hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)
        except NoResultFound:
            raise ValueError("Invalid reset token")
