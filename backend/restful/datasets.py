from flask import Blueprint, request, make_response, send_from_directory, send_file
import flask_restx
import context
import flask_jwt_extended
import os
from restful.auth import admin_login_required
import shutil


datasets_blueprint = Blueprint("Datasets-API", __name__)
api = flask_restx.Api(datasets_blueprint)


class DatasetsList(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        # Return list of datasets
        datasets_path = context.config["datasets_path"]
        return_list = []

        datasets = os.listdir(datasets_path)

        for dataset in datasets:
            if dataset.startswith("."):
                continue

            dataset_path = os.path.join(datasets_path, dataset)
            if not os.path.isdir(dataset_path):
                continue

            filenames = os.listdir(dataset_path)
            for filename in filenames:
                if filename.startswith("."):
                    continue

                filename_path = os.path.join(dataset_path, filename)
                if os.path.isfile(filename_path):
                    return_list.append(os.path.join(dataset, filename))
                pass
            pass

        result = {
            "code": 0,
            "msg": "success.",
            "data": {"datasets": return_list},
        }
        return result


class DatasetsDownload(flask_restx.Resource):
    def get(self):
        dataset_name = request.args.get("dataset")
        dataset_path = os.path.abspath(os.path.join(context.config["datasets_path"], dataset_name))

        if not os.path.exists(dataset_path):
            result = {
                "code": 11,
                "msg": "Dataset not found.",
                "data": {},
            }
            return result

        # Return dataset file
        response = make_response(
            send_from_directory(os.path.dirname(dataset_path), os.path.basename(dataset_path), as_attachment=True)
        )

        return response


class DatasetsDelete(flask_restx.Resource):
    @admin_login_required
    def post(self):
        body = request.get_json()
        dataset_name = body["dataset"]
        dataset_path = os.path.abspath(os.path.join(context.config["datasets_path"], dataset_name))

        if not os.path.exists(dataset_path):
            result = {
                "code": 11,
                "msg": "Dataset not found.",
                "data": {},
            }
            return result

        os.remove(dataset_path)

        # Return dataset file
        return {"code": 0, "msg": "success."}


class AddDatasetUploaded(flask_restx.Resource):
    parser = flask_restx.reqparse.RequestParser()
    parser.add_argument("file_hash", type=str, location="json")
    parser.add_argument("semantic_specifiction", type=str, location="json")

    @flask_jwt_extended.jwt_required()
    @admin_login_required
    @api.expect(parser)
    def post(self):
        body = request.get_json()
        file_hash = body["file_hash"]
        filename = body["filename"]

        src_file_path = os.path.join(context.config.upload_path, file_hash)
        dst_file_path = os.path.join(context.config.datasets_path, filename)

        shutil.copyfile(src_file_path, dst_file_path)

        return {"code": 0, "msg": "success."}

    pass


api.add_resource(DatasetsList, "/list_datasets")
api.add_resource(DatasetsDownload, "/download_datasets")
api.add_resource(DatasetsDelete, "/delete_datasets")
api.add_resource(AddDatasetUploaded, "/add_dataset_uploaded")
