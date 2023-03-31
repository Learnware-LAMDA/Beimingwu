from flask import Blueprint, g, jsonify, request, session

from config import C
import lib.user as user_interface
from .utils import *


user_api = Blueprint("User-API", __name__)


@user_api.route("/")
def index():
    C.stats += 1
    return f"User API Index {C.stats}"


@user_api.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.user = None if user_id is None else user_interface.get_user_info(by="id", value=user_id)


@user_api.route("/register", methods=["POST"])
def register():
    # Check & get parameters
    data = request.get_json()
    if not check_parameters(data, ["username", "password", "email"]):
        return jsonify({
            "code": 3,
            "msg" : "Request parameters error."
        })
    username = data["username"]
    password = data["password"]
    email = data["email"]
    
    result = {"code": 0, "msg": "Register success."}
    
    # Check uniqueness of user name
    if user_interface.check_user_exist(by="username", value=username):
        result["code"] = 1
        result["msg"] = "Username already exist."
        
    # Check uniqueness of email
    if user_interface.check_user_exist(by="email", value=email):
        result["code"] = 2
        result["msg"] = "Email already exist."
    
    # Add user
    if result["code"] == 0:
        flag = user_interface.add_user(username, password, email, 0, username)
        if not flag: 
            result["code"] = 4
            result["msg"] = "System error."
        
    return jsonify(result)


@user_api.route("/login", methods=["POST"])
def login():
    # Check & get parameters
    data = request.get_json()
    if not check_parameters(data, ["email", "password"]):
        return jsonify({
            "code": 3,
            "msg" : "Request parameters error."
        })
    
    # Try to login
    result = {"code": 0, "msg": "Login success."}
    user = user_interface.get_user_info(by="email", value=data["email"])
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


@user_api.route("/logout", methods=["POST"])
def logout():
    # Check login status
    if g.user is None:
        return jsonify({"code": 1, "msg": "Login required."})
    
    # Logout
    session.clear()
    result = {"code": 0, "msg": "Logout success."}
    return jsonify(result)


@user_api.route("/get_profile", methods=["POST"])
def get_profile():
    # Check login status
    if g.user is None:
        return jsonify({"code": 1, "msg": "Login required."})
    
    # Return profile
    result = {
        "code": 0,
        "msg": "Get profile success.",
        "data": {"username": g.user["username"], "email": g.user["email"]},
    }
    return jsonify(result)
