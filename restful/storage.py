import flask_restx
import flask
import flask_jwt_extended
import werkzeug.datastructures
import context
import os
import lib.engine as engine_helper
import lib.database_operations as dbops
import json


storage_blueprint = flask.Blueprint("STORAGE-API", __name__)
api = flask_restx.Api(storage_blueprint)


parser_chunked_upload = flask_restx.reqparse.RequestParser()
parser_chunked_upload.add_argument("chunk_begin", type=int, required=True, location="form")
parser_chunked_upload.add_argument("file_hash", type=str, required=True, location="form")
parser_chunked_upload.add_argument("chunk_file", type=werkzeug.datastructures.FileStorage, location="files")

@api.route("/chunked_upload")
class ChunkedUpload(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @api.expect(parser_chunked_upload)
    def post(self):
        file = flask.request.files["chunk_file"]
        file_hash = flask.request.form["file_hash"]
        chunk_begin = int(flask.request.form["chunk_begin"])
        file_path = os.path.join(context.config.upload_path, file_hash)
        
        os.makedirs(context.config.upload_path, exist_ok=True)

        with open(file_path, "ab+") as fout:
            fout.seek(chunk_begin)
            fout.write(file.stream.read())
            pass

        return {"code": 0, "msg": "success"}, 200


parser_add_learnware_uploaded = flask_restx.reqparse.RequestParser()
parser_add_learnware_uploaded.add_argument("file_hash", type=str, location="json")
parser_add_learnware_uploaded.add_argument("semantic_specifiction", type=str, location="json")
@api.route("/add_learnware_uploaded")
class AddLearnwareUploaded(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    @api.expect(parser_add_learnware_uploaded)
    def post(self):
        body = flask.request.get_json()
        semantic_specification_str = body.get("semantic_specification")

        semantic_specification, err_msg = engine_helper.parse_semantic_specification(
            semantic_specification_str)
        if semantic_specification is None:
            return {"code": 41, "msg": err_msg}, 200
        
        learnware_id = dbops.get_next_learnware_id()
        src_file_path = os.path.join(context.config.upload_path, body["file_hash"])
        dst_file_path = context.get_learnware_verify_file_path(learnware_id)

        os.rename(src_file_path, dst_file_path)
        learnware_path = context.get_learnware_verify_file_path(learnware_id)
        learnware_semantic_spec_path = learnware_path[:-4] + ".json"

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
        cnt = dbops.add_learnware(user_id, learnware_id)
        if cnt > 0:
            result = {"code": 0, "msg": f"Add success.", "data": {"learnware_id": learnware_id}}
        else:
            result = {
                "code": 31,
                "msg": "System error.",
            }
        
        return result, 200