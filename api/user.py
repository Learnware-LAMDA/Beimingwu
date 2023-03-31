from flask import (
    Blueprint, g, jsonify, request, session
)

from config import C
from lib.user import *


user_api = Blueprint("User-API", __name__)

@user_api.route("/")
def index():
    C.stats += 1
    return f"User API Index {C.stats}"


@user_api.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        email = data['email']
        result = {
            'code': 0,
            'msg': 'Register success.'
        }
        if check_user_exist(by='username', value=username):
            result['code'] = 1
            result['msg'] = 'Username already exist.'
        elif check_user_exist(by='email', value=email):
            result['code'] = 2
            result['msg'] = 'Email already exist.'
        else:
            add_user(username, password, email, 0, username)

        return jsonify(result)


@user_api.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = get_user_info(by='email', value=data['email'])
        result = {
            'code': 0,
            'msg': 'Login success.'
        }
        if user is None:
            result['code'] = 1
            result['msg'] = 'Account not exist.'
        elif not user['password'] == data['password']:
            result['code'] = 2
            result['msg'] = 'Incorrect password.'
        else:
            session.clear()
            session['user_id'] = user['id']

        return jsonify(result)


@user_api.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_user_info(by='id', value=user_id)


@user_api.route('/logout', methods=['POST'])
def logout():
    if g.user is None:
        result = {
            'code': 1,
            'msg': "Login required."
        }
    else:
        session.clear()
        result = {
            'code': 0,
            'msg': 'Logout success.'
        }

    return jsonify(result)


@user_api.route('/get_profile', methods=['POST'])
def get_profile():
    if g.user is None:
        result = {
            'code': 1,
            'msg': "Login required."
        }
    else:
        result = {
            'code': 0,
            'msg': 'Get profile success.',
            'data': {
                'username': g.user['username'],
                'email': g.user['email']
            }
        }

    return jsonify(result)