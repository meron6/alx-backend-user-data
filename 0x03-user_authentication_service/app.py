#!/usr/bin/env python3
""" Flask app for user authentication service """

from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

# Initialize Flask app and Auth object
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def welcome():
    """ Return a JSON welcome message """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'])
def register_user():
    """ Register a new user """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """ Log in a user, create a session ID and store it in a cookie """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(jsonify({"email": email, "message": "logged in"}))
        response.set_cookie('session_id', session_id)
        return response

    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """ Log out the user, destroy the session and redirect to GET / """
    session_id = request.cookies.get('session_id')

    if session_id and AUTH.get_user_from_session_id(session_id):
        AUTH.destroy_session(session_id)
        return redirect('/')

    abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """ Get user profile information using session_id cookie """
    session_id = request.cookies.get('session_id')

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200

    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """ Generate reset password token for a registered user """
    email = request.form.get('email')

    if not email:
        abort(403)

    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """ Update the user's password using reset token """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(403)

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
