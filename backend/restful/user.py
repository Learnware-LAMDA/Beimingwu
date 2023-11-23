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
from learnware.market import EasySemanticChecker
from context import config as C
from . import auth
import flask_jwt_extended
import flask_restx as flask_restful
import flask_bcrypt
import lib.data_utils as data_utils
import uuid
from . import common_functions
from lib import redis_utils


user_blueprint = Blueprint("USER-API", __name__)
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
            "data": {"user_id": user_id, "username": user["username"], "email": user["email"], "role": user["role"]},
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
        print(f"change password for user_id: {user_id}")

        user = database.get_user_info(by="id", value=user_id)

        if user is None:
            return {"code": 51, "msg": "Account not exist."}, 200
        elif not flask_bcrypt.check_password_hash(user["password"], old_value):
            return {"code": 52, "msg": "Incorrect password."}, 200

        new_passwd_hash = flask_bcrypt.generate_password_hash(new_value).decode("utf-8")
        flag = database.update_user_password(pwd=new_passwd_hash, by="id", value=user_id)

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
        is_verified = body.get("is_verified", None)

        user_id = flask_jwt_extended.get_jwt_identity()
        if is_verified is None:
            rows, cnt = database.get_learnware_list_by_user_id(user_id, limit=limit, page=page)
        else:
            rows, cnt = database.get_learnware_list("user_id", user_id, limit=limit, page=page, is_verified=is_verified)

        learnware_list = []
        for row in rows:
            learnware_info = dict()
            learnware_info["learnware_id"] = row["learnware_id"]
            learnware_info["last_modify"] = row["last_modify"].strftime("%Y-%m-%d %H:%M:%S.%f %Z")
            learnware_info["verify_status"] = row["verify_status"]

            learnware_info["semantic_specification"] = data_utils.get_learnware_semantic_specification(learnware_info)
            print(
                f'learnware_id: {learnware_info["learnware_id"]}, semantic_specification: {learnware_info["semantic_specification"]}'
            )

            learnware_list.append(learnware_info)

        result = {
            "code": 0,
            "msg": "Ok.",
            "data": {
                "learnware_list": learnware_list,
                "page": page,
                "limit": limit,
                "total_pages": (cnt + limit - 1) // limit,
            },
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

        learnware_file.seek(0)
        learnware_file.save(learnware_path)

        result, retcd = common_functions.add_learnware(learnware_path, semantic_specification, learnware_id)

        return result, retcd


class UpdateLearnwareApi(flask_restful.Resource):
    parser = flask_restful.reqparse.RequestParser()
    parser.add_argument("learnware_id", type=str, required=True, location="form")
    parser.add_argument("semantic_specification", type=str, required=True, location="form")
    parser.add_argument("learnware_file", type=werkzeug.datastructures.FileStorage, location="files")

    @api.expect(parser)
    @flask_jwt_extended.jwt_required()
    def post(self):
        semantic_specification_str = request.form.get("semantic_specification")
        learnware_id = request.form.get("learnware_id")
        user_id = flask_jwt_extended.get_jwt_identity()

        learnware_info = database.get_learnware_by_learnware_id(learnware_id)

        if user_id != learnware_info["user_id"] and not database.check_user_admin(user_id):
            return {"code": 31, "msg": "Permission denied."}, 200

        verify_status = learnware_info["verify_status"]
        if verify_status == LearnwareVerifyStatus.PROCESSING.value:
            return {"code": 51, "msg": "Learnware is verifying."}, 200

        semantic_specification, err_msg = engine_helper.parse_semantic_specification(semantic_specification_str)
        if semantic_specification is None:
            return {"code": 41, "msg": err_msg}, 200

        learnware_file = None
        if request.files is not None:
            learnware_file = request.files.get("learnware_file")
        learnware_path = context.get_learnware_verify_file_path(learnware_id)
        learnware_semantic_spec_path = learnware_path[:-4] + ".json"

        learnware_in_engine = context.engine.get_learnware_by_ids(learnware_id) is not None

        if learnware_file is None:
            if EasySemanticChecker.check_semantic_spec(semantic_specification) == EasySemanticChecker.INVALID_LEARNWARE:
                return {"code": 41, "msg": "Semantic specification check failed!"}, 200
            learnware_path = None
        else:
            learnware_file.seek(0)
            learnware_file.save(learnware_path)
            check_result, msg = engine_helper.check_learnware_file(semantic_specification, learnware_path)
            if not check_result:
                return {"code": 51, "msg": msg}, 200
            pass

        database.update_learnware_timestamp(learnware_id)

        if learnware_in_engine:
            context.engine.update_learnware(
                id=learnware_id,
                zip_path=learnware_path,
                semantic_spec=semantic_specification,
                checker_names=[],
                check_status=EasySemanticChecker.NONUSABLE_LEARNWARE,
            )

            redis_utils.publish_reload_learnware(learnware_id)
        else:
            with open(learnware_semantic_spec_path, "w") as f:
                json.dump(semantic_specification, f)
                pass
            pass

        database.update_learnware_verify_result(learnware_id, LearnwareVerifyStatus.WAITING, "")

        return {"code": 0, "msg": "success"}, 200


class DeleteLearnwareApi(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        body = request.get_json()
        learnware_id = body.get("learnware_id")

        if learnware_id is None:
            return {"code": 21, "msg": "Request parameters error."}, 200

        learnware_id = body["learnware_id"]
        user_id = flask_jwt_extended.get_jwt_identity()

        if database.check_user_admin(user_id):
            user_id = database.get_user_id_by_learnware(learnware_id)

        return common_functions.delete_learnware(user_id, learnware_id)


@api.doc(params={"learnware_id": "learnware id"})
class VerifyLog(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def get(self):
        user_id = flask_jwt_extended.get_jwt_identity()
        learnware_id = request.args.get("learnware_id")

        # check if user is admin
        if database.check_user_admin(user_id):
            result = database.get_verify_log(None, learnware_id)
        else:
            result = database.get_verify_log(user_id, learnware_id)
            pass

        return {"code": 0, "data": result}, 200


class CreateToken(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        user_id = flask_jwt_extended.get_jwt_identity()
        token = uuid.uuid4().hex

        database.create_user_token(user_id, token)

        return {"code": 0, "data": {"token": token}}, 200


class ListToken(flask_restful.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        user_id = flask_jwt_extended.get_jwt_identity()

        result = database.get_user_tokens(user_id)

        result = {"token_list": result}

        return {"code": 0, "data": result}, 200


class DeleteToken(flask_restful.Resource):
    parser = flask_restful.reqparse.RequestParser()
    parser.add_argument("token", type=str, required=True, help="token", location="json")

    @api.expect(parser)
    @flask_jwt_extended.jwt_required()
    def post(self):
        user_id = flask_jwt_extended.get_jwt_identity()
        token = request.get_json().get("token")

        if token is None:
            return {"code": 21, "msg": "Request parameters error."}, 200

        database.delete_user_token(user_id, token)

        return {"code": 0, "msg": "success"}, 200


class ChunkedUpload(flask_restful.Resource):
    parser = flask_restful.reqparse.RequestParser()
    parser.add_argument("chunk_begin", type=int, required=True, location="form")
    parser.add_argument("file_hash", type=str, required=True, location="form")
    parser.add_argument("chunk_file", type=werkzeug.datastructures.FileStorage, location="files")

    @flask_jwt_extended.jwt_required()
    @api.expect(parser)
    def post(self):
        file = request.files["chunk_file"]
        file_hash = request.form["file_hash"]
        chunk_begin = int(request.form["chunk_begin"])
        file_path = os.path.join(context.config.upload_path, file_hash)

        os.makedirs(context.config.upload_path, exist_ok=True)

        with open(file_path, "ab+") as fout:
            fout.seek(chunk_begin)
            fout.write(file.stream.read())

        return {"code": 0, "msg": "success"}, 200


class AddLearnwareUploaded(flask_restful.Resource):
    parser = flask_restful.reqparse.RequestParser()
    parser.add_argument("file_hash", type=str, location="json")
    parser.add_argument("semantic_specifiction", type=str, location="json")

    @flask_jwt_extended.jwt_required()
    @api.expect(parser)
    def post(self):
        body = request.get_json()
        semantic_specification_str = body.get("semantic_specification")

        semantic_specification, err_msg = engine_helper.parse_semantic_specification(semantic_specification_str)
        if semantic_specification is None:
            return {"code": 41, "msg": err_msg}, 200

        learnware_id = database.get_next_learnware_id()
        src_file_path = os.path.join(context.config.upload_path, body["file_hash"])
        dst_file_path = context.get_learnware_verify_file_path(learnware_id)

        os.rename(src_file_path, dst_file_path)
        learnware_path = dst_file_path

        result, retcd = common_functions.add_learnware(learnware_path, semantic_specification, learnware_id)

        return result, retcd

    pass


api.add_resource(ProfileApi, "/profile")
api.add_resource(ChangePasswordApi, "/change_password")
api.add_resource(ListLearnwareApi, "/list_learnware")
api.add_resource(AddLearnwareApi, "/add_learnware")
api.add_resource(UpdateLearnwareApi, "/update_learnware")
api.add_resource(DeleteLearnwareApi, "/delete_learnware")
api.add_resource(VerifyLog, "/verify_log")
api.add_resource(AddLearnwareUploaded, "/add_learnware_uploaded")
api.add_resource(ChunkedUpload, "/chunked_upload")
api.add_resource(CreateToken, "/create_token")
api.add_resource(ListToken, "/list_token")
api.add_resource(DeleteToken, "/delete_token")
