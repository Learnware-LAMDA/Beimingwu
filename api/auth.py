import functools
from flask import Blueprint, g, jsonify, request, session
from config import C
from .utils import *
if C.database_type == "sqlite": import lib.sql_user as user_db

__all__ = ["auth_api", "login_required", "admin_login_required"]

auth_api = Blueprint("AUTH-API", __name__)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({"code": 1, "msg": "Login required."})
        return view(**kwargs)
    return wrapped_view

def admin_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({"code": 1, "msg": "Login required."})
        if g.user["role"] != 1:
            return jsonify({"code": 11, "msg": "Admin account required."})
        return view(**kwargs)
    return wrapped_view

@auth_api.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = None if user_id is None else user_db.get_user_info(by="id", value=user_id)


@auth_api.route("/register", methods=["POST"])
def register():
    # Check & get parameters
    data = get_parameters(request, ["username", "password", "email"])
    if data is None:
        return jsonify({
            "code": 3,
            "msg" : "Request parameters error."
        })
    username = data["username"]
    password = data["password"]
    email = data["email"]
    
    result = {"code": 0, "msg": "Register success."}
    
    # Check uniqueness of user name
    if user_db.check_user_exist(by="username", value=username):
        result["code"] = 1
        result["msg"] = "Username already exist."
        
    # Check uniqueness of email
    if user_db.check_user_exist(by="email", value=email):
        result["code"] = 2
        result["msg"] = "Email already exist."
    
    # Add user
    if result["code"] == 0:
        flag = user_db.add_user(username, password, email, 0, username)
        if not flag: 
            result["code"] = 4
            result["msg"] = "System error."
        
    return jsonify(result)


@auth_api.route("/login", methods=["POST"])
def login():
    # Check & get parameters
    data = get_parameters(request, ["email", "password"])
    if data is None:
        return jsonify({
            "code": 3,
            "msg" : "Request parameters error."
        })
    
    # Try to login
    result = {"code": 0, "msg": "Login success."}
    user = user_db.get_user_info(by="email", value=data["email"])
    if user is None:
        result["code"] = 1
        result["msg"] = "Account not exist."
    elif not user["password"] == data["password"]:
        result["code"] = 2
        result["msg"] = "Incorrect password."
    else:
        session.clear()
        session["user_id"] = user["id"]

    return jsonify(result)


@auth_api.route("/logout", methods=["POST"])
def logout():
    # Check login status
    if g.user is None:
        return jsonify({"code": 1, "msg": "Login required."})
    
    # Logout
    session.clear()
    result = {"code": 0, "msg": "Logout success."}
    return jsonify(result)