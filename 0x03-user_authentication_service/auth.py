#!/usr/bin/env python3
""" This module contains a method that hashes a string.
"""
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
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
