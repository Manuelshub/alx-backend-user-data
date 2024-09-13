#!/usr/bin/env python3
""" This module contains a method that hashes a string.
"""
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash a password for storing.

    Args:
        password (str): The password to hash

    Returns:
        The hashed password in bytes
    """
    hash_salt = bcrypt.gensalt()
    byte_pwd = password.encode('utf-8')
    hashed_pwd = bcrypt.hashpw(byte_pwd, hash_salt)

    return hashed_pwd


def _generate_uuid() -> str:
    """ Genereates string representation of a new UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user in the database.

        Args:
            email (str): The user's email address
            password (str): The user's password

        Returns:
            User: The new User instance
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hash_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hash_pwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Verifies a user's credentials.

        Args:
            email (str): The user's email address
            password (str): The user's password

        Returns:
            bool: True if the credentials are valid, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """
        Generates a new session ID for the given user and
        stores it in the database.

        Args:
            email (str): The user's email address

        Returns:
            str: The new session ID
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        sess_id = _generate_uuid()
        self._db.update_user(user.id, session_id=sess_id)
        return sess_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieves a user from the database given a session ID.

        Args:
            session_id (str): The session ID of the user to retrieve.

        Returns:
            User: The user associated with the given session ID, or None if no
                user is found.
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user
