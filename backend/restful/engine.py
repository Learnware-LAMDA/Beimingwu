import io
import zipfile
import tempfile
from flask import Blueprint, Response, jsonify, request
from flask import send_from_directory, send_file, make_response
import uuid
import context
from context import config as C
import os, json, time
import lib.engine as adv_engine
from database.base import LearnwareVerifyStatus
from .utils import dump_learnware, get_parameters, generate_random_str
import flask_jwt_extended
import flask_restx as flask_restful
import traceback
import lib.database_operations as dbops
import lib.data_utils as data_utils
from learnware.market import BaseChecker
from learnware.config import C as learnware_conf
from lib import redis_utils


engine_blueprint = Blueprint("Engine-API", __name__)
api = flask_restful.Api(engine_blueprint)


class SematicSpecification(flask_restful.Resource):
    @flask_jwt_extended.jwt_required(optional=True)
    def get(
        self,
    ):
        try:
            result = {
                "code": 0,
                "msg": "Ok",
                "data": {"semantic_specification": context.engine_config.semantic_specs},
            }
            return result, 200
        except:
            return {"code": 41, "msg": "Engine get semantic specification error."}, 200


class SearchLearnware(flask_restful.Resource):
    @flask_jwt_extended.jwt_required(optional=True)
    def post(self):
        # Load name & semantic specification

        user_id = flask_jwt_extended.get_jwt_identity()

        semantic_str = request.form.get("semantic_specification")
        is_verified = request.form.get("is_verified", "true")
        learnware_id = request.form.get("learnware_id", None)
        is_hetero = False

        if semantic_str is None:
            return {"code": 21, "msg": f"Request parameters error."}, 200
        context.logger.info(f"search learnware, semantic_str: {semantic_str}")

        # Check statistical specification
        if request.files is None:
            statistical_str = None
        elif "statistical_specification" not in request.files:
            statistical_str = None
        else:
            statistical_file = request.files["statistical_specification"]
            statistical_str = statistical_file.read()

        # Acquire check_status
        if is_verified == "false":
            if user_id is None or not dbops.check_user_admin(user_id):
                return {"code": 61, "msg": "cannot search unverified learnware."}, 200

            check_status = BaseChecker.NONUSABLE_LEARNWARE
        else:
            check_status = BaseChecker.USABLE_LEARNWARE

        # Load semantic specification
        try:
            semantic_specification = json.loads(semantic_str)
        except:
            return {"code": 41, "msg": "Semantic specification error"}, 200

        # Learnware id search
        if learnware_id is not None:
            if user_id is None or not dbops.check_user_admin(user_id):
                return {"code": 61, "msg": "cannot search learnware by id."}, 200
            semantic_specification["learnware_id"] = {"Values": learnware_id, "Type": "String"}

        if statistical_str is None:
            status, msg, ret = adv_engine.search_learnware_by_semantic(
                semantic_specification, user_id, check_status=check_status
            )
        else:
            status, msg, ret = adv_engine.search_learnware(
                semantic_specification, statistical_str, user_id, check_status=check_status
            )
            if ret is not None:
                is_hetero = ret[-1]
                ret = ret[:-1]
            pass

        print(msg)

        if not status:
            return {"code": 41, "msg": msg}, 200

        (matching, single_learnware_list, multi_score, multi_learnware) = ret
        print(f"single learnware list after search in engine: {len(single_learnware_list)}")
        print(f"matching score after search in engine: {matching}")
        if matching is None and multi_learnware is None:  # result of seach learnware with no statistical specification
            matching = [0 for _ in single_learnware_list]
            multi_learnware = []

        assert len(matching) == len(single_learnware_list)
        n = len(single_learnware_list)

        # Try paging
        limit = request.form.get("limit")
        page = request.form.get("page")
        try:
            limit = int(limit)
        except:
            limit = None

        # Process learnware list
        mul_list, sin_list = [], []
        for x in multi_learnware:
            try:
                learnware_id = x.id
                learnware = context.engine.get_learnware_by_ids(learnware_id)

                mul_list.append(dump_learnware(learnware, multi_score))
            except Exception as err:
                print(err)
                traceback.print_exc()
                pass
        for i in range(n):
            try:
                learnware_id = single_learnware_list[i].id
                learnware = context.engine.get_learnware_by_ids(learnware_id)
                sin_list.append(dump_learnware(learnware, matching[i]))
            except Exception as err:
                print(err)
                traceback.print_exc()
                pass
        n = len(sin_list)

        # Directly whole list
        if limit is None:
            result = {
                "code": 0,
                "msg": "Ok",
                "data": {
                    "learnware_list_multi": mul_list,
                    "learnware_list_single": sin_list,
                    "is_hetero": is_hetero,
                },
            }
            self.set_learnware_info(result["data"]["learnware_list_single"])
            self.set_learnware_info(result["data"]["learnware_list_multi"])
            return result, 200

        # Paging
        if limit == 0:
            return {"code": 52, "msg": "Limit cannot be 0."}, 200
        try:
            page = int(page)
        except:
            page = 0

        result = {
            "code": 0,
            "msg": "Ok",
            "data": {
                "learnware_list_multi": [],
                "learnware_list_single": [],
                "is_hetero": is_hetero,
                "page": page,
                "limit": limit,
                "total_pages": (n + limit - 1) // limit,
            },
        }
        if page == 0:
            result["data"]["learnware_list_multi"] = mul_list
            pass

        result["data"]["learnware_list_single"] = [
            sin_list[i] for i in range(page * limit, min(n, page * limit + limit))
        ]

        self.set_learnware_info(result["data"]["learnware_list_single"])
        self.set_learnware_info(result["data"]["learnware_list_multi"])

        dbops.add_log(
            name="search_learnware",
            info=json.dumps(
                {
                    "user_id": user_id,
                }
            ),
        )

        return result, 200
        pass

    def set_learnware_info(self, learnware_list):
        learnware_ids = [learnware["learnware_id"] for learnware in learnware_list]
        ts = dbops.get_learnware_timestamps(learnware_ids)
        usernames = dbops.get_learnware_owners(learnware_ids)

        for i in range(len(learnware_list)):
            learnware_list[i]["last_modify"] = ts[i].strftime("%Y-%m-%d %H:%M:%S.%f %Z")
            learnware_list[i]["username"] = usernames[i]
            pass
        pass


class DownloadLearnware(flask_restful.Resource):
    @flask_jwt_extended.jwt_required(optional=True)
    def get(self):
        user_id = flask_jwt_extended.get_jwt_identity()
        learnware_id = request.args.get("learnware_id")

        if learnware_id is None:
            return {"code": 21, "msg": "Request parameters error."}, 200

        learnware_info = dbops.get_learnware_by_learnware_id(learnware_id)

        if learnware_info["verify_status"] != LearnwareVerifyStatus.SUCCESS.value:
            # it is an unverified learnware
            if user_id is None:
                return {"code": 61, "msg": "cannot download unverified learnware."}, 200
            elif user_id != learnware_info["user_id"]:
                if not dbops.check_user_admin(user_id):
                    return {"code": 62, "msg": "cannot download unverified learnware."}, 200
                pass
            pass

        try:
            learnware_zip_path = context.engine.get_learnware_zip_path_by_ids(learnware_id)
        except:
            return {"code": 42, "msg": "Engine download learnware error."}, 200

        if learnware_zip_path is None:
            learnware_zip_path = context.get_learnware_verify_file_path(learnware_id)
            pass

        zip_directory = os.path.dirname(learnware_zip_path)
        zip_filename = os.path.basename(learnware_zip_path)
        response = make_response(send_from_directory(zip_directory, zip_filename, as_attachment=True))

        dbops.add_log(
            name="download_learnware",
            info=json.dumps(
                {
                    "learnware_id": learnware_id,
                }
            ),
        )
        return response


class GenerateDownloadToken(flask_restful.Resource):
    parser = flask_restful.reqparse.RequestParser()
    parser.add_argument("learnware_ids", type=list, location="json")

    @flask_jwt_extended.jwt_required(optional=True)
    @api.expect(parser)
    def post(self):
        user_id = flask_jwt_extended.get_jwt_identity()
        body = request.get_json()
        learnware_ids = body.get("learnware_ids")

        if learnware_ids is None:
            return {"code": 21, "msg": "Request parameters error."}, 200

        for learnware_id in learnware_ids:
            learnware_info = dbops.get_learnware_by_learnware_id(learnware_id)

            if learnware_info["verify_status"] != LearnwareVerifyStatus.SUCCESS.value:
                # it is an unverified learnware
                if user_id is None:
                    return {"code": 61, "msg": "cannot download unverified learnware."}, 200
                elif user_id != learnware_info["user_id"]:
                    if not dbops.check_user_admin(user_id):
                        return {"code": 62, "msg": "cannot download unverified learnware."}, 200
                    pass
                pass
            pass

        token = uuid.uuid4().hex
        redis_utils.add_learnware_download_token(learnware_ids, token)
        return {"code": 0, "data": {"token": token}}, 200

    pass


class DownloadByToken(flask_restful.Resource):
    parser = flask_restful.reqparse.RequestParser()
    parser.add_argument("token", type=str, location="params")

    def get(self):
        token = request.args.get("token")
        learnware_ids = redis_utils.get_learnware_id_from_download_token(token)
        if learnware_ids is None:
            return {"code": 21, "msg": "token not exist."}, 200

        learnware_id = learnware_ids[0]
        try:
            learnware_zip_path = context.engine.get_learnware_zip_path_by_ids(learnware_id)
        except:
            return {"code": 42, "msg": "Engine download learnware error."}, 200

        if learnware_zip_path is None:
            learnware_zip_path = context.get_learnware_verify_file_path(learnware_id)
            pass

        zip_directory = os.path.dirname(learnware_zip_path)
        zip_filename = os.path.basename(learnware_zip_path)
        response = make_response(send_from_directory(zip_directory, zip_filename, as_attachment=True))

        dbops.add_log(
            name="download_learnware",
            info=json.dumps(
                {
                    "learnware_id": learnware_id,
                }
            ),
        )
        return response
        pass

    pass


class LearnwareInfo(flask_restful.Resource):
    def get(self):
        learnware_id = request.args.get("learnware_id")

        if learnware_id is None:
            return {"code": 21, "msg": "Request parameters error."}, 200

        learnware_info = dbops.get_learnware_by_learnware_id(learnware_id)

        if learnware_info is None:
            return {"code": 41, "msg": "Learnware not found."}, 200

        try:
            learnware_info["semantic_specification"] = data_utils.get_learnware_semantic_specification(learnware_info)
        except Exception as e:
            traceback.print_exc()
            return {"code": 42, "msg": "Engine find learnware error."}, 200

        result = {"code": 0, "msg": "Ok", "data": {"learnware_info": learnware_info}}

        return result, 200

    pass


class DownloadMultiLearnware(flask_restful.Resource):
    @flask_jwt_extended.jwt_required(optional=True)
    def get(self):
        learnware_ids = request.args.getlist("learnware_ids")

        if learnware_ids is None or not isinstance(learnware_ids, list) or len(learnware_ids) > 10:
            return {"code": 21, "msg": "Request parameters error."}, 200

        user_id = flask_jwt_extended.get_jwt_identity()
        if user_id is not None:
            user_is_admin = dbops.check_user_admin(user_id)
        else:
            user_is_admin = False
            pass

        for learnware_id in learnware_ids:
            learnware_info = dbops.get_learnware_by_learnware_id(learnware_id)
            if learnware_info["verify_status"] != LearnwareVerifyStatus.SUCCESS.value:
                # it is an unverified learnware
                if user_id is None:
                    return {"code": 61, "msg": "cannot download unverified learnware."}, 200
                elif user_id != learnware_info["user_id"]:
                    if not user_is_admin:
                        return {"code": 62, "msg": "cannot download unverified learnware."}, 200
                    pass
                pass
            pass

        try:
            learnware_paths = [
                context.engine.get_learnware_zip_path_by_ids(learnware_id) for learnware_id in learnware_ids
            ]
        except:
            return {"code": 42, "msg": "Engine download learnware error."}, 200

        if None in learnware_paths:
            return {"code": 41, "msg": "Learnware not found."}, 200

        with tempfile.TemporaryDirectory(prefix="multi_learnware_") as tempdir:
            zip_filename = "multiple_learnwares.zip"
            zip_filename = os.path.join(tempdir, zip_filename)
            with zipfile.ZipFile(zip_filename, "w") as zip_file:
                for learnware_path in learnware_paths:
                    filename = os.path.basename(learnware_path)
                    zip_file.write(learnware_path, arcname=filename)

            res = send_file(zip_filename, as_attachment=True)
            os.remove(zip_filename)
            return res


class DownloadMultiLearnwareByToken(flask_restful.Resource):
    parser = flask_restful.reqparse.RequestParser()
    parser.add_argument("token", type=str, location="params")

    @api.expect(parser)
    def get(self):
        token = request.args.get("token")
        learnware_ids = redis_utils.get_learnware_id_from_download_token(token)
        if learnware_ids is None:
            return {"code": 21, "msg": "token not exist."}, 200

        try:
            learnware_paths = [
                context.engine.get_learnware_zip_path_by_ids(learnware_id) for learnware_id in learnware_ids
            ]
        except:
            return {"code": 42, "msg": "Engine download learnware error."}, 200

        if None in learnware_paths:
            return {"code": 41, "msg": "Learnware not found."}, 200

        with tempfile.TemporaryDirectory(prefix="multi_learnware_") as tempdir:
            zip_filename = "multiple_learnwares.zip"
            zip_filename = os.path.join(tempdir, zip_filename)
            with zipfile.ZipFile(zip_filename, "w") as zip_file:
                for learnware_path in learnware_paths:
                    filename = os.path.basename(learnware_path)
                    zip_file.write(learnware_path, arcname=filename)

            res = send_file(zip_filename, as_attachment=True)
            os.remove(zip_filename)
            return res


api.add_resource(SematicSpecification, "/semantic_specification")
api.add_resource(SearchLearnware, "/search_learnware")
api.add_resource(DownloadLearnware, "/download_learnware")
api.add_resource(LearnwareInfo, "/learnware_info")
api.add_resource(DownloadMultiLearnware, "/download_multi_learnware")
api.add_resource(DownloadMultiLearnwareByToken, "/download_multi_learnware_by_token")
api.add_resource(GenerateDownloadToken, "/generate_download_token")
api.add_resource(DownloadByToken, "/download_by_token")
