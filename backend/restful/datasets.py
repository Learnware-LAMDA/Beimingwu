from flask import Blueprint, request, make_response, send_from_directory, send_file
import flask_restx
import context
import flask_jwt_extended
import os


datasets_blueprint = Blueprint("Datasets-API", __name__)
api = flask_restx.Api(datasets_blueprint)


class DatasetsList(flask_restx.Resource):
    @flask_jwt_extended.jwt_required()
    def post(self):
        # Return list of datasets
        datasets_path = context.config["datasets_path"]

        datasets = os.listdir(datasets_path)
        datasets = [
            dataset
            for dataset in datasets
            if (not dataset.startswith(".")) and os.path.isfile(os.path.join(datasets_path, dataset))
        ]

        result = {
            "code": 0,
            "msg": "success.",
            "data": {"datasets": datasets},
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
        response = make_response(send_from_directory(os.path.dirname(dataset_path), dataset_name, as_attachment=True))

        return response


api.add_resource(DatasetsList, "/list_datasets")
api.add_resource(DatasetsDownload, "/download_datasets")
