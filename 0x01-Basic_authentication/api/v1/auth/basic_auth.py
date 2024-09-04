#!/usr/bin/env python3
""" This module contains  a class for API Authentication
"""
from .auth import Auth
import base64
import binascii


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
            val = base64.b64decode(base64_authorization_header)
        except binascii.Error:
            return None
        return val.decode('utf-8')

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
        vals = decoded_base64_authorization_header.split(':')
        return vals[0], vals[1]
