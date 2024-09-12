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
    Auth.create_session(email)
    return jsonify({"email": email, "message": "logged in"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
