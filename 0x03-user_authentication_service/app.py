#!/usr/bin/env python3
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def welcome() -> str:
    """ GET /
    Return:
        - welcome message
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """ POST /users
    Return:
        - user creation status message
    """
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Handle missing email or password
    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def sessions_login() -> str:
    """ POST /sessions
    Return:
        - login status message
    """
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Handle missing email or password
    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    valid_login = AUTH.valid_login(email, password)
    if valid_login:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def sessions_logout() -> str:
    """ DELETE /sessions
    Return:
        - logout status message
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    
    if user:
        AUTH.destroy_session(user.id)
        # Clear the session_id cookie upon logout
        response = redirect('/')
        response.delete_cookie('session_id')
        return response
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ GET /profile
    Return:
        - user profile information
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    
    if user:
        return jsonify({"email": user.email, "message": "profile found"}), 200
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
