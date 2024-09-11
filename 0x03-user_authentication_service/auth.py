#!/usr/bin/env python3
""" This module contains a method that hashes a string.
"""
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
