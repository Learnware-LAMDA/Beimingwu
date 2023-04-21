from flask import Blueprint, g, jsonify, request
from config import C
import hashlib
from .auth import admin_login_required
from .user import remove_learnware
from .utils import get_parameters, generate_random_str

if C.database_type == "sqlite":
    import lib.sqlite as database

import lib.engine as engine_helper

admin_api = Blueprint("Admin-API", __name__)


@admin_api.route("/")
def index():
    C.stats += 1
    return f"Admin API Index {C.stats}"


@admin_api.route("/get_user_list", methods=["POST"])
@admin_login_required
def get_user_list():
    data = get_parameters(request, [])
    
    # Get like parameters
    username = None if data is None or "username" not in data else data["username"]
    email    = None if data is None or "email"    not in data else data["email"]
    
    # Return whole user list directly
    if data is None or "limit" not in data:
        ret, cnt = database.get_all_user_list(
            columns=["id", "username", "email"], 
            username=username, 
            email=email
        )
        result = {
            "code": 0,
            "msg": "Get user list success.",
            "data": {"user_list": ret}
        }
        return jsonify(result)
    
    # Calculate the page limit
    limit = data["limit"]
    if limit == 0:
        return jsonify({"code": 51, "msg": "Limit cannot be 0."})
    page  = 0 if "page" not in data else data["page"]
    
    ret, cnt = database.get_all_user_list(
        columns=["id", "username", "email"], 
        limit=limit, page=page, 
        username=username, email=email
    )
    result = {
        "code": 0,
        "msg": "Get user list success.",
        "data": {
            "user_list": ret,
            "page": page,
            "limit": limit,
            "total_pages": (cnt + limit - 1) // limit
        }
    }
    return jsonify(result)

@admin_api.route("/delete_user", methods=["POST"])
@admin_login_required
def delete_user():
    # Check & get parameters
    data = get_parameters(request, ["user_id"])
    if data is None:
        return jsonify({"code": 21, "msg": "Request parameters error."})
    user_id = data["user_id"]

    # Check user existence
    if not database.check_user_exist("id", user_id):
        return jsonify({"code": 51, "msg": "User not found."})

    # Check learnware
    ret, cnt = database.get_learnware_list("user_id", user_id)
    if len(ret) > 0:
        learnware_list = engine_helper.get_learnware_by_id([x["learnware_id"] for x in ret])
        return jsonify({
            "code": 52, 
            "msg": "Learnware list is not empty.", 
            "data": {
                "learnware_list": learnware_list
            }
        })

    # Delete user
    cnt = database.remove_user("id", user_id)
    if cnt > 0:
        result = {"code": 0, "msg": "Delete success."}
    else:
        result = {
            "code": 31,
            "msg": "System error.",
        }
    return jsonify(result)


@admin_api.route("/get_learnware_list", methods=["POST"])
@admin_login_required
def get_learnware_list():
    data = get_parameters(request, [])
    # Return whole user list directly
    if data is None or "limit" not in data:
        ret, cnt = database.get_all_learnware_list(columns=["user_id", "learnware_id", "last_modify"])
        learnware_list = engine_helper.get_learnware_by_id([x["learnware_id"] for x in ret])
        result = {
            "code": 0,
            "msg": "Get learnware list success.",
            "data": {
                "learnware_list": learnware_list
            }
        }
        return jsonify(result)
    # Calculate the page limit
    limit = data["limit"]
    if limit == 0:
        return jsonify({"code": 51, "msg": "Limit cannot be 0."})
    page  = 0 if "page" not in data else data["page"]
    ret, cnt = database.get_all_learnware_list(columns=["user_id", "learnware_id", "last_modify"], limit=limit, page=page)
    learnware_list = engine_helper.get_learnware_by_id([x["learnware_id"] for x in ret])
    result = {
        "code": 0,
        "msg": "Get learnware list success.",
        "data": {
            "learnware_list": learnware_list,
            "page": page,
            "limit": limit,
            "total_pages": (cnt + limit - 1) // limit
        }
    }
    return jsonify(result)


@admin_api.route("/delete_learnware", methods=["POST"])
@admin_login_required
def delete_learnware():
    # Check & get parameters
    data = get_parameters(request, ["learnware_id"])
    if data is None:
        return jsonify({"code": 21, "msg": "Request parameters error."})
    learnware_id = data["learnware_id"]

    # Check permission
    learnware = database.get_learnware_list("learnware_id", learnware_id)
    if len(learnware) == 0:
        return jsonify({"code": 51, "msg": "Learnware not found."})

    # Remove learnware
    if remove_learnware(learnware_id):
        result = {"code": 0, "msg": "Delete success."}
    else:
        result = {
            "code": 31,
            "msg": "System error.",
        }
    return jsonify(result)

@admin_api.route("/reset_password", methods=["POST"])
@admin_login_required
def reset_password():
    data = get_parameters(request, ["id"])
    if data is None: 
        return jsonify({"code": 21, "msg": "Request parameters error."})
    user_id = data["id"]
    user = database.get_user_info(by="id", value=user_id)
    password = generate_random_str(8)
    md5 = hashlib.md5(password.encode("utf-8")).hexdigest()
    if user is None:
        return jsonify({"code": 51, "msg": "Account not exist."})
    flag = database.update_user_password(pwd=md5, by="id", value=user_id)
    if not flag:
        return jsonify({"code": 31, "msg": "Update error."})
    
    # Return profile
    result = {
        "code": 0,
        "msg": "Reset success",
        "data":{
            "password": password,
            "md5": md5
        }
    }
    return jsonify(result)