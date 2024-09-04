#!/usr/bin/env python3
""" This module contains a class for API Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class for managing the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to check if the given path requires authentication

        Args:
            path (str): The path to check
            excluded_paths (List[str]): A list of paths that don't require auth

        Returns:
            bool: True if path requires auth, False otherwise
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        for a_path in excluded_paths:
            if a_path[-1] == '/' and path == a_path[:-1]:
                return False
            if path != a_path:
                return True
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the value of the Authorization header from a request.
        If request is not provided, it uses the current request context.
        Returns None if the header is not found.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.

        Args:
            request (Request): The request to check (default is None)

        Returns:
            User: The current user, or None if not found
        """
        return None
