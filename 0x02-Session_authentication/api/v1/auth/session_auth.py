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
