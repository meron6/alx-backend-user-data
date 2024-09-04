#!/usr/bin/env python3
""" Users view module """

from flask import Blueprint, jsonify, request, abort
from models.user import User

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/users', methods=['GET'])
def get_users():
    """ Retrieves all users """
    if request.current_user is None:
        abort(401)
    users = User.all()
    return jsonify([user.to_json() for user in users])

@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """ Retrieves a user by ID """
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        user = request.current_user
    else:
        user = User.get(user_id)
        if user is None:
            abort(404)
    return jsonify(user.to_json())

@users_blueprint.route('/users', methods=['POST'])
def create_user():
    """ Creates a new user """
    # Implement user creation logic
    pass

@users_blueprint.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ Updates an existing user """
    # Implement user update logic
    pass

@users_blueprint.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Deletes a user """
    # Implement user deletion logic
    pass
