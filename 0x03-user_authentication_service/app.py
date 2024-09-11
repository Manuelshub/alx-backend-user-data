#!/usr/bin/env python3
"""
This module contains a flask app
"""
from auth import Auth
from flask import Flask, jsonify, request


app = Flask(__name__)
Auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def default():
    """ Returns a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """ Registers a user
    """
    if request:
        email = request.form.get("email")
        password = request.form.get("password")
    try:
        user = Auth.register_user(email, password)
        return jsonify({
            "email": email,
            "message": "user created"
        }), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)
