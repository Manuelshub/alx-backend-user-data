#!/usr/bin/env python3
""" This methid contains a class that inherits from SessionAuth
"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ This class inherits from the SessionAuth class
    """

    def __init__(self):
        """ Initialize
        """
        try:
            session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """
        Creates a session for a user.

        Args:
            user_id (str): The id of the user to create a session for.

        Returns:
            str: The session ID.
        """

        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        SessionAuth.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the User ID based on a Session ID.

        Args:
            session_id (str): The Session ID to look up.

        Returns:
            str: The User ID related to the Session ID.
        """
        if session_id is None:
            return None
        if session_id not in SessionAuth.user_id_by_session_id.keys():
            return None
        session_dict = SessionAuth.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict['user_id']
        if 'created_at' not in session_dict.keys():
            return None
        created_time = session_dict['created_at']
        time_delta = timedelta(seconds=self.session_duration)
        if (created_time + time_delta) < datetime.now():
            return None
        return session_dict['user_id']
