#!/usr/bin/env python3
"""Representation of BasicAuth class
"""

import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar, Tuple, Optional

class BasicAuth(Auth):
    """BasicAuth class for Basic Authentication.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> Optional[str]:
        """Extract base64 part from the Authorization header.

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            Optional[str]: Base64 encoded part of the header or None if invalid.
        """
        if authorization_header and isinstance(authorization_header, str) and authorization_header.startswith("Basic "):
            return authorization_header.split(" ")[1]
        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) -> Optional[str]:
        """Decode base64 encoded string.

        Args:
            base64_authorization_header (str): Base64 encoded string.

        Returns:
            Optional[str]: Decoded string or None if decoding fails.
        """
        if base64_authorization_header and isinstance(base64_authorization_header, str):
            try:
                decoded = base64.b64decode(base64_authorization_header).decode('utf-8')
                return decoded
            except (base64.binascii.Error, UnicodeDecodeError):
                return None
        return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract user credentials from decoded string.

        Args:
            decoded_base64_authorization_header (str): Decoded credentials string.

        Returns:
            Tuple[Optional[str], Optional[str]]: Tuple of email and password or (None, None) if invalid.
        """
        if decoded_base64_authorization_header and isinstance(decoded_base64_authorization_header, str) and ":" in decoded_base64_authorization_header:
            email, password = decoded_base64_authorization_header.split(":", 1)
            return (email, password)
        return (None, None)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> Optional[TypeVar('User')]:
        """Retrieve user object based on email and password.

        Args:
            user_email (str): User email.
            user_pwd (str): User password.

        Returns:
            Optional[TypeVar('User')]: User object if valid, otherwise None.
        """
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                users = User.search({"email": user_email})
                for user in users:
                    if user.is_valid_password(user_pwd):
                        return user
            except Exception:
                return None
        return None

    def current_user(self, request=None) -> Optional[TypeVar('User')]:
        """Get the current user from the request.

        Args:
            request (Optional[Request]): Flask request object.

        Returns:
            Optional[TypeVar('User')]: Current user object or None if not found.
        """
        header = self.authorization_header(request)
        b64header = self.extract_base64_authorization_header(header)
        decoded = self.decode_base64_authorization_header(b64header)
        user_creds = self.extract_user_credentials(decoded)
        return self.user_object_from_credentials(*user_creds)
