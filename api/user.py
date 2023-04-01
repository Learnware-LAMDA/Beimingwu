from flask import Blueprint, g, jsonify, request, session

from config import C
from .utils import *
from .auth import login_required
if C.database_type == "sqlite": import lib.sql_user as user_db
user_api = Blueprint("User-API", __name__)

@user_api.route("/get_profile", methods=["POST"])
@login_required
def get_profile():
    # Return profile
    result = {
        "code": 0,
        "msg": "Get profile success.",
        "data": {"username": g.user["username"], "email": g.user["email"]},
    }
    return jsonify(result)

@user_api.route("/get_learnware_list", methods=["POST"])
@login_required
def get_learnware_list():
    # Return profile
    result = {
        "code": 0,
        "msg": "Ok.",
        "data": user_db.get_learnware_list("user_id", g.user["id"])
    }
    return jsonify(result)

@user_api.route("/add_learnware", methods=["POST"])
@login_required
def add_learnware():
    # Check & get parameters
    # data = get_parameters(request, ["description"])
    # if data is None:
    #     return jsonify({
    #         "code": 2,
    #         "msg" : "Request parameters error."
    #     })
    # learnware_id = data["learnware_id"]
    # [TODO] Require code for engine
    
    user_id = g.user["id"]
    learnware_id = generate_random_str(16)
    
    # Add learnware 
    cnt = user_db.add_learnware(user_id, learnware_id)
    if cnt > 0:
        result = {
            "code": 0,
            "msg": f"Add {cnt} learnware.",
            "data": learnware_id
        }
    else:
        result = {
            "code": 3,
            "msg": "System error.",
        }
    return jsonify(result)

@user_api.route("/delete_learnware", methods=["POST"])
@login_required
def delete_learnware():
    # Check & get parameters
    data = get_parameters(request, ["learnware_id"])
    if data is None:
        return jsonify({
            "code": 2,
            "msg" : "Request parameters error."
        })
    learnware_id = data["learnware_id"]
    
    # Check permission
    learnware = user_db.get_learnware_list("learnware_id", learnware_id)
    if len(learnware) == 0 or learnware[0]["user_id"] != g.user["id"]:
        return jsonify({
            "code": 3,
            "msg" : "You do not own this learnware."
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
            "code": 4,
            "msg": "System error.",
        }
    return jsonify(result)