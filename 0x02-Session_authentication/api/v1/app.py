#!/usr/bin/env python3
""" Main module """

from flask import Flask, request
from api.v1.auth.auth import Auth
from models.user import User
from api.v1.views.users import users_blueprint

app = Flask(__name__)
app.register_blueprint(users_blueprint, url_prefix='/api/v1')

auth = Auth()

@app.before_request
def before_request():
    """ Assign the current user to request.current_user """
    request.current_user = auth.current_user(request)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
