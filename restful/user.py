from flask import Blueprint, g, jsonify, request, session
import werkzeug.datastructures
import json
import os
import shutil
from .utils import *

import lib.database_operations as database

import lib.engine as engine_helper
from database.base import LearnwareVerifyStatus
import context
from context import config as C
from . import auth
import flask_jwt_extended
import flask_restx as flask_restful
import flask_bcrypt
import lib.data_utils as data_utils


user_blueprint = Blueprint("api", __name__)
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
        # ret, cnt = database.get_learnware_list("user_id", user_id, limit=limit, page=page, is_verified=True)
        rows, cnt = database.get_learnware_list_by_user_id(user_id, limit=limit, page=page)

        learnware_list = []
        for row in rows:
            learnware_info = dict()
            learnware_info["learnware_id"] = row["learnware_id"]
            learnware_info["verify_status"] = row["verify_status"]

            learnware_info["semantic_specification"] = data_utils.get_learnware_semantic_specification(
                learnware_info)
            print(f'learnware_id: {learnware_info["learnware_id"]}, semantic_specification: {learnware_info["semantic_specification"]}')

            learnware_list.append(learnware_info)
            
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


class ListLearnwareUnverifiedApi(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        body = request.get_json()
        keys = ["limit", "page"]
        if any([k not in body for k in keys]):
            return {"code": 21, "msg": "Request parameters error."}, 200
        
        limit = body["limit"]
        page = body["page"]

        user_id = flask_jwt_extended.get_jwt_identity()
        ret, cnt = database.get_learnware_list("user_id", user_id, limit=limit, page=page, is_verified=False)

        # read semantic specification
        learnware_list = []
        for row in ret:
            learnware_id = row["learnware_id"]
            learnware_info = dict()
            semantic_spec_path = context.get_learnware_verify_file_path(learnware_id)[:-4] + ".json"
            with open(semantic_spec_path, "r") as f:
                learnware_info["semantic_specification"] = json.load(f)
                pass
            learnware_info["learnware_id"] = learnware_id
            learnware_list.append(learnware_info)
            pass
        

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


class AddLearnwareApi(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        semantic_specification_str = request.form.get("semantic_specification")

        print(semantic_specification_str)
        semantic_specification, err_msg = engine_helper.parse_semantic_specification(semantic_specification_str)
        if semantic_specification is None:
            return {"code": 41, "msg": err_msg}, 200
        
        learnware_file = request.files.get("learnware_file")
        if learnware_file is None or learnware_file.filename == "":
            return {"code": 21, "msg": "Request parameters error."}, 200
        
        learnware_id = database.get_next_learnware_id()

        if not os.path.exists(C.upload_path):
            os.mkdir(C.upload_path)

        learnware_path = context.get_learnware_verify_file_path(learnware_id)
        learnware_semantic_spec_path = learnware_path[:-4] + ".json"

        learnware_file.seek(0)
        learnware_file.save(learnware_path)

        # check learnware file
        check_result, msg = engine_helper.check_learnware_file(
            semantic_specification, learnware_path)

        if not check_result:
            return {"code": 51, "msg": msg}, 200
        
        with open(learnware_semantic_spec_path, "w") as f:
            json.dump(semantic_specification, f)
            pass

        user_id = flask_jwt_extended.get_jwt_identity()

        # Add learnware
        cnt = database.add_learnware(user_id, learnware_id)
        if cnt > 0:
            result = {"code": 0, "msg": f"Add success.", "data": {"learnware_id": learnware_id}}
        else:
            result = {
                "code": 31,
                "msg": "System error.",
            }
        
        return result, 200
    pass


parser_update_learnware = flask_restful.reqparse.RequestParser()
parser_update_learnware.add_argument("learnware_id", type=str, required=True, location="form")
parser_update_learnware.add_argument("semantic_specification", type=str, required=True, location="form")
parser_update_learnware.add_argument("learnware_file", type=werkzeug.datastructures.FileStorage, location="files")
class UpdateLearnwareApi(flask_restful.Resource):
    @api.expect(parser_update_learnware)
    @flask_jwt_extended.jwt_required()
    def post(self):
        semantic_specification_str = request.form.get("semantic_specification")
        learnware_id = request.form.get("learnware_id")

        print(semantic_specification_str)
        semantic_specification, err_msg = engine_helper.parse_semantic_specification(semantic_specification_str)
        if semantic_specification is None:
            return {"code": 41, "msg": err_msg}, 200
        
        learnware_file = None
        if request.files is not None:
            learnware_file = request.files.get("learnware_file")
            pass

        learnware_path = context.get_learnware_verify_file_path(learnware_id)
        learnware_semantic_spec_path = learnware_path[:-4] + ".json"
        with open(learnware_semantic_spec_path, "w") as f:
            json.dump(semantic_specification, f)
            pass
        if learnware_file is not None:
            learnware_file.seek(0)
            learnware_file.save(learnware_path)
            pass

        verify_status = database.get_learnware_verify_status(learnware_id)

        if verify_status == LearnwareVerifyStatus.PROCESSING.value:
            return {"code": 51, "msg": "Learnware is verifying."}, 200
        
        elif verify_status == LearnwareVerifyStatus.SUCCESS.value:
            # this learnware is verified
            print(f'update verified learnware: {learnware_id}')

            if learnware_file is None:
                learnware_path_origin = context.engine.get_learnware_path_by_ids(learnware_id)
                shutil.copyfile(learnware_path_origin, learnware_path)
                pass
            context.engine.delete_learnware(learnware_id)
            database.update_learnware_verify_result(learnware_id, LearnwareVerifyStatus.WAITING, "")
            pass
        else:
            pass
        
        return {"code": 0, "msg": "success"}, 200
        

class AddLearnwareVerifiedApi(flask_restful.Resource):
    # todo: this api should be protected
    def post(self):
        body = request.get_json()

        learnware_id = body["learnware_id"]
        learnware_file = context.get_learnware_verify_file_path(learnware_id)
        learnware_semantic_spec_path = learnware_file[:-4] + ".json"

        with open(learnware_semantic_spec_path, "r") as f:
            semantic_specification = json.load(f)
            pass
        
        context.engine.add_learnware(learnware_file, semantic_specification, learnware_id=learnware_id)

        os.remove(learnware_file)
        os.remove(learnware_semantic_spec_path)

        return {"code": 0, "msg": "success"}, 200
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

        print(f'delete learnware: {learnware_id}')

        # Check permission
        learnware_infos, cnt = database.get_learnware_list("learnware_id", learnware_id)
        if len(learnware_infos) == 0:
            return {"code": 51, "msg": "Learnware not exist."}, 200
        
        if learnware_infos[0]["user_id"] != user_id:
            return {"code": 41, "msg": "You do not own this learnware."}, 200
        
        learnware_info = learnware_infos[0]

        if learnware_info['verify_status'] == LearnwareVerifyStatus.SUCCESS.value:
            ret = context.engine.delete_learnware(learnware_id)
            if not ret:
                return {"code": 42, "msg": "Engine delete learnware error."}, 200
            pass
        else:
            # Delete learnware file
            learnware_path = context.get_learnware_verify_file_path(learnware_id)
            learnware_sematic_spec_path = learnware_path[:-4] + ".json"
            os.remove(learnware_path)
            os.remove(learnware_sematic_spec_path)
            pass
        
        cnt = database.remove_learnware("learnware_id", learnware_id)

        result = {"code": 0, "msg": "Delete success."}
        return result, 200
    pass


@api.doc(params={'learnware_id': 'learnware id'})
class VerifyLog(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def get(self):
        user_id = flask_jwt_extended.get_jwt_identity()
        learnware_id = request.args.get("learnware_id")

        result = database.get_verify_log(user_id, learnware_id)

        return {"code": 0, "data": result}, 200
    pass


api.add_resource(ProfileApi, "/profile")
api.add_resource(ChangePasswordApi, "/change_password")
api.add_resource(ListLearnwareApi, "/list_learnware")
api.add_resource(ListLearnwareUnverifiedApi, "/list_learnware_unverified")
api.add_resource(AddLearnwareApi, "/add_learnware")
api.add_resource(UpdateLearnwareApi, "/update_learnware")
api.add_resource(AddLearnwareVerifiedApi, "/add_learnware_verified")
api.add_resource(DeleteLearnwareApi, "/delete_learnware")
api.add_resource(VerifyLog, "/verify_log")

