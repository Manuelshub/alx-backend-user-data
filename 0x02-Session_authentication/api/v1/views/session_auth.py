#!/usr/bin/env python3
""" This module contains the endpoint for session login
"""
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    Session Login
    """
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    # Using import statement here to avoid circular import
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    cookie_resp = getenv('SESSION_NAME')
    user_dict = jsonify(user.to_json())

    user_dict.set_cookie(cookie_resp, session_id)
    return user_dict


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    """
    Deletes the user session / logout
    """
    # Importing here to avoid circular import
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
