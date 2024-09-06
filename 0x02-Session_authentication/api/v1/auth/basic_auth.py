#!/usr/bin/env python3
""" This module contains  a class for API Authentication
"""
from .auth import Auth
import base64
import binascii
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """ This class inherits from the Auth class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header.

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            str: The Base64 part of the Authorization header.
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        else:
            return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        Decodes the Base64 part of the Authorization header.

        Args:
            base64_authorization_header (str):
                The Base64 part of the Authorization header.

        Returns:
            str: The decoded value of the Base64 part of the
                Authorization header.
        """
        if base64_authorization_header is None or type(
             base64_authorization_header) is not str:
            return None
        try:
            encode = base64_authorization_header.encode('utf-8')
            val = base64.b64decode(encode)
            return val.decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Extracts the user email and password from the decoded Base64
        authorization header

        Args:
            decoded_base64_authorization_header (str):
                The decoded Base64 authorization header

        Returns:
            tuple: A tuple containing the user email and password
        """
        if decoded_base64_authorization_header is None or type(
             decoded_base64_authorization_header) is not str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        vals = decoded_base64_authorization_header.split(':', 1)
        return vals[0], vals[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Retrieves the User instance based on his email and password.

        Args:
            user_email (str): The email of the user to retrieve.
            user_pwd (str): The password of the user to retrieve.

        Returns:
            User: The User instance requested.
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for the current request.

        Args:
            request (Request): The current request object.

        Returns:
            User: The User instance for the current request.
        """
        auth_header = self.authorization_header(request)
        if auth_header:
            token = self.extract_base64_authorization_header(auth_header)
            if token:
                dcd = self.decode_base64_authorization_header(token)
                if dcd:
                    u_name, u_pwd = self.extract_user_credentials(dcd)
                    if u_name and u_pwd:
                        return self.user_object_from_credentials(u_name, u_pwd)
        return
