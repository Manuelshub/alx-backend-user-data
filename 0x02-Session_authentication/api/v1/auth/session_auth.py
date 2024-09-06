#!/usr/bin/env python3
""" Module contains a class that inherits from Auth.
"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """ This class inherits from Auth class.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session for a user.

        Args:
            user_id (str): The id of the user to create a session for.

        Returns:
            str: The session ID.
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the User ID based on a Session ID.

        Args:
            session_id (str): The Session ID to look up.

        Returns:
            str: The User ID related to the Session ID.
        """
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)
