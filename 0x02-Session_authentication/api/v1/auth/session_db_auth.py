#!/usr/bin/env python3

"""
SessionDBAuth module
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from os import getenv
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class.
    """

    def create_session(self, user_id=None):
        """
        Creates a session for a user.
        """
        if user_id:
            session_id = super().create_session(user_id)
            if not session_id:
                return None
            new_user_session = UserSession(user_id=user_id, session_id=session_id)
            new_user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user_id for a given session_id.
        """
        if not session_id:
            return None
        try:
            user_sessions = UserSession.search({'session_id': session_id})
            for user_session in user_sessions:
                created_at = user_session.get('created_at')
                if not created_at or (datetime.now() > created_at + timedelta(seconds=self.session_duration)):
                    return None
                return user_session.get('user_id')
        except Exception:
            return None

    def destroy_session(self, request=None) -> bool:
        """
        Destroys the session associated with a request.
        """
        if request:
            session_id = self.session_cookie(request)
            if session_id and super().destroy_session(request):
                try:
                    user_sessions = UserSession.search({'session_id': session_id})
                    for user_session in user_sessions:
                        user_session.remove()
                        return True
                except Exception:
                    return False
        return False
