#!/usr/bin/env python3
""" SessionExpAuth module
"""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv

class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class.
    """

    def __init__(self):
        """ Constructor.
        """
        duration = getenv('SESSION_DURATION')
        self.session_duration = int(duration) if duration and duration.isdigit() else 0

    def create_session(self, user_id=None):
        """ Creates a session.
        """
        session_id = super().create_session(user_id) if user_id else None
        if session_id:
            session_dict = {'user_id': user_id, 'created_at': datetime.now()}
            self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieves the user_id for a session_id.
        """
        if session_id:
            session_dict = self.user_id_by_session_id.get(session_id)
            if session_dict:
                user_id = session_dict['user_id']
                session_start = session_dict['created_at']
                if self.session_duration <= 0 or datetime.now() <= session_start + timedelta(seconds=self.session_duration):
                    return user_id
        return None
