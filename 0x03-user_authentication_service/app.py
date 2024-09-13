#!/usr/bin/env python3
"""
This module contains a flask app
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

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
    if valid:
        session_id = Auth.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})
        res.set_cookie('session_id', session_id)
        return res
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ Logs out a user
    """
    session_id = request.cookies.get("session_id")
    user = Auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    Auth.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    Returns a JSON payload based on the user session.
    """
    session_id = request.cookies.get("session_id")
    user = Auth.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
