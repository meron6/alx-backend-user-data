#!/usr/bin/env python3
from flask import Flask, request, jsonify, abort, redirect, make_response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()

# Task 6: Basic Flask app with "Bienvenue" message
@app.route('/', methods=['GET'])
def welcome():
    return jsonify({"message": "Bienvenue"})

# Task 7: Register user
@app.route('/users', methods=['POST'])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

# Task 11: Log in
@app.route('/sessions', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(jsonify({"email": email, "message": "logged in"}))
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)

# Task 14: Log out
@app.route('/sessions', methods=['DELETE'])
def logout():
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)

# Task 15: User profile
@app.route('/profile', methods=['GET'])
def profile():
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)

# Task 17: Get reset password token
@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)

# Task 19: Update password
@app.route('/reset_password', methods=['PUT'])
def update_password():
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
