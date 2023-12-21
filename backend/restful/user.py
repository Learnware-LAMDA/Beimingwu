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
from lib import sensitive_words_utils
from lib import common_utils


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

        file_hash = common_utils.get_file_hash(learnware_path)
        if database.get_learnware_id_by_file_hash(file_hash) is not None:
            return {"code": 61, "msg": "Learnware file already exist."}, 200

        result, retcd = common_functions.add_learnware(learnware_path, semantic_specification, learnware_id)

        if result["code"] == 0:
            database.add_file_hash(learnware_id, file_hash)
            pass

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
        if learnware_info is None:
            return {"code": 71, "msg": "Learnware id does not exist."}, 200

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
            result, msg = engine_helper.check_semantic_spec(semantic_specification)
            if result == False:
                return {"code": 51, "msg": msg}, 200
            learnware_path = None
        else:
            learnware_file.seek(0)
            learnware_file.save(learnware_path)
            file_hash = common_utils.get_file_hash(learnware_path)
            learnware_id_by_file_hash = database.get_learnware_id_by_file_hash(file_hash)
            if learnware_id_by_file_hash is not None and learnware_id_by_file_hash != learnware_id:
                return {"code": 61, "msg": "Learnware file already exist."}, 200
            check_result, msg = engine_helper.check_learnware_file(semantic_specification, learnware_path)
            if not check_result:
                return {"code": 51, "msg": msg}, 200
            pass

        database.update_learnware_timestamp(learnware_id)

        if learnware_in_engine:
            check_flag, check_status = True, EasySemanticChecker.NONUSABLE_LEARNWARE

            old_semantic_specification = data_utils.get_learnware_semantic_specification(learnware_info)
            if (
                learnware_file is None
                and old_semantic_specification.get("Data", {}) == semantic_specification.get("Data", {})
                and old_semantic_specification.get("Task", {}) == semantic_specification.get("Task", {})
                and old_semantic_specification.get("Input", {}) == semantic_specification.get("Input", {})
                and old_semantic_specification.get("Output", {}) == semantic_specification.get("Output", {})
            ):
                check_flag = False
                if verify_status == LearnwareVerifyStatus.SUCCESS.value:
                    check_status = EasySemanticChecker.USABLE_LEARWARE

            context.engine.update_learnware(
                id=learnware_id,
                zip_path=learnware_path,
                semantic_spec=semantic_specification,
                checker_names=[],
                check_status=check_status,
            )
            redis_utils.publish_reload_learnware(learnware_id)
            if check_flag:
                database.update_learnware_verify_result(learnware_id, LearnwareVerifyStatus.WAITING, "")
        else:
            with open(learnware_semantic_spec_path, "w") as f:
                json.dump(semantic_specification, f)
            database.update_learnware_verify_result(learnware_id, LearnwareVerifyStatus.WAITING, "")

        if learnware_file is not None:
            database.add_file_hash(learnware_id, file_hash)
            pass

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

        if chunk_begin == 0:
            # it is first chunk
            if database.get_learnware_id_by_file_hash(file_hash) is not None:
                return {"code": 51, "msg": "Learnware file already exist."}, 200
            pass

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
        file_hash = body["file_hash"]

        semantic_specification, err_msg = engine_helper.parse_semantic_specification(semantic_specification_str)
        if semantic_specification is None:
            return {"code": 41, "msg": err_msg}, 200

        learnware_id = database.get_next_learnware_id()

        if database.get_learnware_id_by_file_hash(file_hash) is not None:
            return {"code": 61, "msg": "Learnware file already exist."}, 200

        src_file_path = os.path.join(context.config.upload_path, file_hash)
        dst_file_path = context.get_learnware_verify_file_path(learnware_id)

        os.rename(src_file_path, dst_file_path)
        learnware_path = dst_file_path

        result, retcd = common_functions.add_learnware(learnware_path, semantic_specification, learnware_id)

        if result["code"] == 0:
            database.add_file_hash(learnware_id, file_hash)
            pass

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
