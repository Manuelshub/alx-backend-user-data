#!/usr/bin/env python3
"""
This module contains a flask app
"""
from auth import Auth
from flask import Flask, jsonify, request, abort

Auth = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def default() -> str:
    """ Returns a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """ Registers a user
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        Auth.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ Login a user
    """
    email = request.form.get("email")
    password = request.form.get("password")
    valid = Auth.valid_login(email, password)
    if not valid:
        abort(401)
    else:
        session_id = Auth.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie('session_id', session_id)
        return res


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ Logs out a user
    """
    session_id = request.cookies.get("session_id")
    try:
        user_id = Auth.get_user_from_session_id(session_id)
    except NoResultFound:
        abort(403)
    return jsonify({"email": user.email}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
