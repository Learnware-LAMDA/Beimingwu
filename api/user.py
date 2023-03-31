import functools

from flask import (
    Blueprint, g, jsonify, redirect, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from config import C
from lib.user import *


user_api = Blueprint("User-API", __name__)

@user_api.route("/")
def index():
    C.stats += 1
    return f"User API Index {C.stats}"


@user_api.route('/register', methods=['GET', 'POST'])
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
            add_user(username, generate_password_hash(password), email, 0, username)

        return jsonify(result)


@user_api.route('/login', methods=['GET', 'POST'])
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
        elif not check_password_hash(user['password'], data['password']):
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


@user_api.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))

        return view(**kwargs)

    return wrapped_view
