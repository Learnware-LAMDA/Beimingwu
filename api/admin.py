from flask import Blueprint, g, jsonify, request
from config import C
from .auth import admin_login_required
if C.database_type == "sqlite": import lib.sql_user as user_db

admin_api = Blueprint("Admin-API", __name__)

@admin_api.route("/")
def index():
    C.stats += 1
    return f"Admin API Index {C.stats}"

@admin_api.route("/get_user_list", methods=["POST"])
@admin_login_required
def get_user_list():
    if g.user is None:
        result = {"code": 1, "msg": "Login required."}
    elif g.user["role"] != 1:
        result = {"code": 2, "msg": "Permission denied."}
    else:
        result = {"code": 0, "msg": "Get user list success."}
        result["data"] = user_db.get_all_user_info(columns=["username", "email"])
    return jsonify(result)

@admin_api.route("/delete_user", methods=["POST"])
@admin_login_required
def delete_user():
    if g.user is None:
        result = {"code": 1, "msg": "Login required."}
    elif g.user["role"] != 1:
        result = {"code": 2, "msg": "Permission denied."}
    else:
        result = {"code": 0, "msg": "Get user list success."}
        result["data"] = user_db.get_all_user_info(columns=["username", "email"])
    return jsonify(result)

@admin_api.route("/get_learnware_list", methods=["POST"])
@admin_login_required
def get_learnware_list():
    if g.user is None:
        result = {"code": 1, "msg": "Login required."}
    elif g.user["role"] != 1:
        result = {"code": 2, "msg": "Permission denied."}
    else:
        result = {"code": 0, "msg": "Get user list success."}
        result["data"] = user_db.get_all_user_info(columns=["username", "email"])
    return jsonify(result)

@admin_api.route("/delete_learnware", methods=["POST"])
@admin_login_required
def delete_learnware():
    if g.user is None:
        result = {"code": 1, "msg": "Login required."}
    elif g.user["role"] != 1:
        result = {"code": 2, "msg": "Permission denied."}
    else:
        result = {"code": 0, "msg": "Get user list success."}
        result["data"] = user_db.get_all_user_info(columns=["username", "email"])
    return jsonify(result)