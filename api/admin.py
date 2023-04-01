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
    result = {
        "code": 0, 
        "msg": "Get user list success.",
        "data": user_db.get_all_user_list(columns=["username", "email"])
    }
    return jsonify(result)

@admin_api.route("/delete_user", methods=["POST"])
@admin_login_required
def delete_user():
    result = {"code": 0, "msg": "Get user list success."}
    result["data"] = user_db.get_all_learnware_list(columns=["user_id", "learnware_id", "last_modify"])
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
    # Check permission
    learnware = user_db.get_learnware_list("learnware_id", learnware_id)
    if len(learnware) == 0:
        return jsonify({
            "code": 32,
            "msg" : "Learnware not found."
        })
    
    # Delete learnware
    # [TODO] Require code for engine
    cnt = user_db.remove_learnware("learnware_id", learnware_id)
    if cnt > 0:
        result = {
            "code": 0,
            "msg": f"Delete {cnt} learnware.",
        }
    else:
        result = {
            "code": 31,
            "msg": "System error.",
        }
    return jsonify(result)