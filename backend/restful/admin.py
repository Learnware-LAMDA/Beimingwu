from flask import Blueprint, request
import context
from context import config as C
from learnware.market import BaseChecker
import hashlib
from .auth import admin_login_required, super_admin_login_required
from .utils import generate_random_str
from . import common_functions

import lib.database_operations as database

import lib.engine as engine_helper
import lib.data_utils as data_utils
import flask_restx as flask_restful
import flask_bcrypt
import flask_jwt_extended


admin_blueprint = Blueprint("Admin-API", __name__)
api = flask_restful.Api(admin_blueprint)


class ListUser(flask_restful.Resource):
    @admin_login_required
    def post(self):
        data = request.get_json()

        # Get like parameters
        username = None if data is None or "username" not in data else data["username"]
        email = None if data is None or "email" not in data else data["email"]

        # Return whole user list directly
        if data is None or "limit" not in data:
            ret, cnt = database.get_all_user_list(
                columns=["id", "username", "email", "role"], username=username, email=email
            )
            result = {"code": 0, "msg": "Get user list success.", "data": {"user_list": ret}}
            return result, 200

        # Calculate the page limit
        limit = data["limit"]
        if limit == 0:
            return {"code": 51, "msg": "Limit cannot be 0."}, 200

        page = 0 if "page" not in data else data["page"]

        ret, cnt = database.get_all_user_list(
            columns=["id", "username", "email", "role"], limit=limit, page=page, username=username, email=email
        )
        result = {
            "code": 0,
            "msg": "Get user list success.",
            "data": {"user_list": ret, "page": page, "limit": limit, "total_pages": (cnt + limit - 1) // limit},
        }
        return result, 200


class DeleteUser(flask_restful.Resource):
    @admin_login_required
    def post(self):
        # Check & get parameters
        data = request.get_json()

        if data is None or "user_id" not in data:
            return {"code": 21, "msg": "Request parameters error."}, 200

        user_id = data["user_id"]

        # Check user existence
        user_info = database.get_user_info(by="id", value=user_id)

        if user_info is None:
            return {"code": 51, "msg": "User not found."}, 200

        op_user_id = flask_jwt_extended.get_jwt_identity()
        op_user_info = database.get_user_info(by="id", value=op_user_id)
        if op_user_info["role"] <= user_info["role"]:
            return {"code": 52, "msg": "cannot delete user with higher priority"}, 200

        # Check learnware
        ret, cnt = database.get_learnware_list("user_id", user_id)
        if len(ret) > 0:
            learnware_list = engine_helper.get_learnware_by_id([x["learnware_id"] for x in ret])
            return {"code": 52, "msg": "Learnware list is not empty.", "data": {"learnware_list": learnware_list}}, 200

        # Delete user
        cnt = database.remove_user("id", user_id)
        if cnt > 0:
            result = {"code": 0, "msg": "Delete success."}
        else:
            result = {
                "code": 31,
                "msg": "System error.",
            }
        return result, 200


class ListLearnware(flask_restful.Resource):
    @admin_login_required
    def post(self):
        data = request.get_json()
        limit = data.get("limit", 10)
        page = data.get("page", 0)
        is_verified = data.get("is_verified", None)
        user_id = data.get("user_id", None)

        rows, cnt = database.get_all_learnware_list(
            columns=["user_id", "learnware_id", "last_modify", "verify_status"],
            limit=limit,
            page=page,
            is_verified=is_verified,
            user_id=user_id,
        )

        datas = []
        for row in rows:
            username = database.get_user_info(by="id", value=row["user_id"])["username"]
            semantic_spec = data_utils.get_learnware_semantic_specification(row)
            data = dict()
            data["username"] = username
            data["semantic_specification"] = semantic_spec
            data["learnware_id"] = row["learnware_id"]
            data["last_modify"] = row["last_modify"].strftime("%Y-%m-%d %H:%M:%S.%f %Z")
            data["verify_status"] = row["verify_status"]
            datas.append(data)

        result = {
            "code": 0,
            "msg": "Ok",
            "data": {
                "learnware_list_single": datas,
                "page": page,
                "limit": limit,
                "total_pages": (cnt + limit - 1) // limit,
            },
        }
        return result, 200


class DeleteLearnware(flask_restful.Resource):
    @admin_login_required
    def post(self):
        body = request.get_json()
        learnware_id = body.get("learnware_id")

        if learnware_id is None:
            return {"code": 21, "msg": "Request parameters error."}, 200

        learnware_id = body["learnware_id"]
        user_id = database.get_user_id_by_learnware(learnware_id)

        print(f"delete learnware: {learnware_id}")

        return common_functions.delete_learnware(user_id, learnware_id)


class ResetPassword(flask_restful.Resource):
    @admin_login_required
    def post(self):
        data = request.get_json()
        if data is None or "id" not in data:
            return {"code": 21, "msg": "Request parameters error."}, 200

        user_id = data["id"]
        user = database.get_user_info(by="id", value=user_id)
        password = generate_random_str(8)
        md5 = hashlib.md5(password.encode("utf-8")).hexdigest()
        if user is None:
            return {"code": 51, "msg": "Account not exist."}, 200

        password_hash = flask_bcrypt.generate_password_hash(md5).decode("utf-8")

        flag = database.update_user_password(pwd=password_hash, by="id", value=user_id)
        if not flag:
            return {"code": 31, "msg": "Update error."}, 200

        # Return profile
        result = {"code": 0, "msg": "Reset success", "data": {"password": password, "md5": md5}}
        return result, 200


class SetUserRole(flask_restful.Resource):
    parser = flask_restful.reqparse.RequestParser()
    parser.add_argument("role", type=str, required=True, location="json")
    parser.add_argument("user_id", type=str, required=True, location="json")

    @super_admin_login_required
    def post(self):
        body = request.get_json()

        if body is None or "role" not in body or "user_id" not in body:
            return {"code": 21, "msg": "Request parameters error."}, 200

        role = body["role"]
        user_id = body["user_id"]

        database.update_user_role(user_id, role)

        return {"code": 0, "msg": "Set user role success."}, 200


class Summary(flask_restful.Resource):
    @admin_login_required
    def post(self):
        count_verified_user = database.get_user_count(is_verified=True)
        count_unverified_user = database.get_user_count(is_verified=False)

        count_verified_learnware = database.get_learnware_count_verified()
        count_download = database.get_download_count()

        count_unverified_learnware_total = database.get_learnware_count_unverified()
        count_unverified_learnware_in_engine = len(
            context.engine.get_learnware_ids(check_status=BaseChecker.NONUSABLE_LEARNWARE)
        )
        count_unverified_learnware_not_in_engine = (
            count_unverified_learnware_total - count_unverified_learnware_in_engine
        )

        count_detail = engine_helper.get_learnware_count_detail()

        count_queued = database.get_learnware_count_queued_or_processing()

        result = {
            "code": 0,
            "msg": "Get summary success.",
            "data": {
                "count_verified_user": count_verified_user,
                "count_unverified_user": count_unverified_user,
                "count_verified_learnware": count_verified_learnware,
                "count_unverified_learnware": count_unverified_learnware_in_engine,
                "count_learnware_awaiting_storage": count_unverified_learnware_not_in_engine,
                "count_download": count_download,
                "count_detail": count_detail,
                "count_queued": count_queued,
            },
        }

        return result, 200


api.add_resource(ListUser, "/list_user")
api.add_resource(DeleteUser, "/delete_user")
api.add_resource(ListLearnware, "/list_learnware")
api.add_resource(DeleteLearnware, "/delete_learnware")
api.add_resource(ResetPassword, "/reset_password")
api.add_resource(Summary, "/summary")
api.add_resource(SetUserRole, "/set_user_role")
