from flask import Blueprint, g, jsonify, request, session
import json
import os, time
import hashlib
from .utils import *

import lib.database_operations as database

import lib.engine as engine_helper
import context
from context import config as C
import flask_jwt_extended
import flask_restful
import flask_bcrypt


user_blueprint = Blueprint("User-API", __name__)
api = flask_restful.Api(user_blueprint)



class ProfileApi(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        # Return profile
        user_id = flask_jwt_extended.get_jwt_identity()
        user = database.get_user_info(by="id", value=user_id)
        result = {
            "code": 0,
            "msg": "Get profile success.",
            "data": {"username": user["username"], "email": user["email"]},
        }
        return result


class ChangePasswordApi(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        body = request.get_json()
        keys = ["old_password", "new_password"]
        if any([k not in body for k in keys]):
            return {"code": 21, "msg": "Request parameters error."}, 200
        
        old_value = body["old_password"]
        new_value = body["new_password"]

        user_id = flask_jwt_extended.get_jwt_identity()
        print(f'change password for user_id: {user_id}')

        user = database.get_user_info(by="id", value=user_id)

        if user is None:
            return {"code": 51, "msg": "Account not exist."}, 200
        elif not flask_bcrypt.check_password_hash(user["password"], old_value):
            return {"code": 52, "msg": "Incorrect password."}, 200
        
        new_passwd_hash = flask_bcrypt.generate_password_hash(new_value).decode("utf-8")
        flag = database.update_user_password(
            pwd=new_passwd_hash, by="id", value=user_id)
        
        if not flag:
            return {"code": 31, "msg": "Update error."}, 200

        # Return profile
        result = {"code": 0, "msg": "Update success"}
        return result, 200
    pass


class ListLearnwareApi(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        body = request.get_json()
        keys = ["limit", "page"]
        if any([k not in body for k in keys]):
            return {"code": 21, "msg": "Request parameters error."}, 200
        
        limit = body["limit"]
        page = body["page"]

        user_id = flask_jwt_extended.get_jwt_identity()
        ret, cnt = database.get_learnware_list("user_id", user_id, limit=limit, page=page)
        learnware_list = engine_helper.get_learnware_by_id([x["learnware_id"] for x in ret])
        result = {
            "code": 0,
            "msg": "Ok.",
            "data": {
                "learnware_list": learnware_list,
                "page": page,
                "limit": limit,
                "total_pages": (cnt + limit - 1) // limit
            }
        }
        return result, 200
    pass


class AddLearnwareApi(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        semantic_specification = request.form.get("semantic_specification")

        # print(semantic_specification)
        try:
            semantic_specification = json.loads(semantic_specification)
        except Exception as e:
            return {"code": 41, "msg": "Semantic specification error"}, 200
        
        learnware_file = request.files.get("learnware_file")
        if learnware_file is None or learnware_file.filename == "":
            return {"code": 21, "msg": "Request parameters error."}, 200
        
        leareware_filename = f"{int(time.time())}_" + hashlib.md5(learnware_file.read()).hexdigest() + ".zip"
        if not os.path.exists(C.upload_path):
            os.mkdir(C.upload_path)
        learnware_path = os.path.join(C.upload_path, leareware_filename)
        learnware_file.seek(0)
        learnware_file.save(learnware_path)

        user_id = flask_jwt_extended.get_jwt_identity()

        learnware_id, retcd = context.engine.add_learnware(learnware_path, semantic_specification)
        # except:
            # return jsonify({"code": 42, "msg": "Engine add learnware error."})
        if retcd == context.engine.INVALID_LEARNWARE:
            return {"code": 42, "msg": "Your learnware is invalid."}, 200
        
        # Add learnware
        cnt = database.add_learnware(user_id, learnware_id)
        if cnt > 0:
            result = {"code": 0, "msg": f"Add success.", "data": {"learnware_id": learnware_id}}
        else:
            result = {
                "code": 31,
                "msg": "System error.",
            }
        
        if C.remove_upload_file: os.remove(learnware_path)
        return result, 200
    pass


class DeleteLearnwareApi(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        body = request.get_json()
        learnware_id= body.get("learnware_id")
        
        if learnware_id is None:
            return {"code": 21, "msg": "Request parameters error."}, 200
        
        learnware_id = body["learnware_id"]
        user_id = flask_jwt_extended.get_jwt_identity()
        # Check permission
        learnware_infos, cnt = database.get_learnware_list("learnware_id", learnware_id)
        if len(learnware_infos) == 0:
            return {"code": 51, "msg": "Learnware not exist."}, 200
        
        if learnware_infos[0]["user_id"] != user_id:
            return {"code": 41, "msg": "You do not own this learnware."}, 200
        
        # Remove learnware
        # [TODO] Require code for engine
        # try:
        ret = context.engine.delete_learnware(learnware_id)
        if not ret:
            return {"code": 42, "msg": "Engine delete learnware error."}, 200
        
        cnt = database.remove_learnware("learnware_id", learnware_id)

        result = {"code": 0, "msg": "Delete success."}
        return result, 200
    pass


api.add_resource(ProfileApi, "/profile")
api.add_resource(ChangePasswordApi, "/change_password")
api.add_resource(ListLearnwareApi, "/list_learnware")
api.add_resource(AddLearnwareApi, "/add_learnware")
api.add_resource(DeleteLearnwareApi, "/delete_learnware")

