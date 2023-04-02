from flask import Blueprint, g, jsonify, request
from config import C
from .auth import admin_login_required
from .user import remove_learnware
from .utils import get_parameters
if C.database_type == "sqlite": import lib.sql_user as user_db

admin_api = Blueprint("Admin-API", __name__)

@admin_api.route("/")
def index():
    C.stats += 1
    return f"Admin API Index {C.stats}"

@admin_api.route("/get_user_list", methods=["POST"])
@admin_login_required
def get_user_list():
    result = {
        "code": 0, 
        "msg": "Get user list success.",
        "data": user_db.get_all_user_list(columns=["id", "username", "email"])
    }
    return jsonify(result)

@admin_api.route("/delete_user", methods=["POST"])
@admin_login_required
def delete_user():
    # Check & get parameters
    data = get_parameters(request, ["user_id"])
    if data is None:
        return jsonify({
            "code": 21,
            "msg" : "Request parameters error."
        })
    user_id = data["user_id"]
    
    # Check user existence
    if not user_db.check_user_exist("id", user_id):
        return jsonify({
            "code": 51,
            "msg": "User not found."
        })
    
    # Check learnware
    learnware_list = user_db.get_learnware_list("user_id", user_id)
    if len(learnware_list) > 0:
        return jsonify({
            "code": 52,
            "msg": "Learnware list is not empty.",
            "data": [x["learnware_id"] for x in learnware_list]
        })
    
    # Delete user
    cnt = user_db.remove_user("id", user_id)
    if cnt > 0:
        result = {
            "code": 0,
            "msg": "Delete success.",
            "data": user_id
        }
    else:
        result = {
            "code": 31,
            "msg": "System error.",
        }
    return jsonify(result)

@admin_api.route("/get_learnware_list", methods=["POST"])
@admin_login_required
def get_learnware_list():
    result = {
        "code": 0, 
        "msg": "Get learnware list success.",
        "data": user_db.get_all_learnware_list(columns=["user_id", "learnware_id", "last_modify"])
    }
    return jsonify(result)

@admin_api.route("/delete_learnware", methods=["POST"])
@admin_login_required
def delete_learnware():
    # Check & get parameters
    data = get_parameters(request, ["learnware_id"])
    if data is None:
        return jsonify({
            "code": 21,
            "msg" : "Request parameters error."
        })
    learnware_id = data["learnware_id"]
    
    # Check permission
    learnware = user_db.get_learnware_list("learnware_id", learnware_id)
    if len(learnware) == 0:
        return jsonify({
            "code": 51,
            "msg" : "Learnware not found."
        })
    
    # Remove learnware
    if remove_learnware(learnware_id):
        result = {
            "code": 0,
            "msg": "Delete success.",
            "data": learnware_id
        }
    else:
        result = {
            "code": 31,
            "msg": "System error.",
        }
    return jsonify(result)