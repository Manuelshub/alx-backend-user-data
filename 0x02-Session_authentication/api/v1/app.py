#!/usr/bin/env python3
"""
Route module for the API

This module sets up the Flask application, registers routes,
handles cross-origin resource sharing (CORS), and configures
authentication based on the environment variable `AUTH_TYPE`.

Authentication can be:
- 'auth': Custom authentication
- 'basic_auth': Basic authentication
- 'session_auth': Session-based authentication

It also sets up custom error handlers for common HTTP errors (404, 401, 403).
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize the appropriate authentication mechanism
auth = None
if getenv('AUTH_TYPE') == 'auth':
    auth = Auth()
elif getenv('AUTH_TYPE') == 'basic_auth':
    auth = BasicAuth()
elif getenv('AUTH_TYPE') == 'session_auth':
    auth = SessionAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handler for 404 Not Found errors.

    Args:
        error: The raised error.

    Returns:
        A JSON response with a 404 status code and an error message.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Handler for 401 Unauthorized errors.

    Args:
        error: The raised error.

    Returns:
        A JSON response with a 401 status code and an error message.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handler for 403 Forbidden errors.

    Args:
        error: The raised error.

    Returns:
        A JSON response with a 403 status code and an error message.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> None:
    """
    Function to be run before every request to filter and check authentication.

    This checks whether the path requires authentication using the
    `require_auth` method of the `auth` object. If authentication is required,
    checks the `Authorization` header and sets the current user for the request

    If no authorization header is present, a 401 error is raised.
    If the user is invalid or missing, a 403 error is raised.

    Special paths that do not require authentication include:
    - '/api/v1/status/'
    - '/api/v1/unauthorized/'
    - '/api/v1/forbidden/'

    Raises:
        401: If the authorization header is missing.
        403: If the user is not authenticated.
    """
    auth_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                  '/api/v1/forbidden/']

    if auth and auth.require_auth(request.path, auth_paths):
        if auth.authorization_header(request) is None:
            abort(401)
        request.current_user = auth.current_user(request)
        if auth.current_user(request) is None:
            abort(403)
        if request.current_user is None:
            abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
