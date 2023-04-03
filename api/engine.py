from flask import Blueprint, jsonify, request
from flask import send_from_directory, send_file, make_response
from .auth import login_required
from config import C
import os

engine_api = Blueprint("Engine-API", __name__)


@engine_api.route("/get_semantic_specification", methods=["GET"])
def get_semantic_specification():
    result = {
        "code": 0,
        "msg": "Ok",
        # "data": C.engine.get_property_list(),
    }
    return jsonify(result)


@engine_api.route("/search_learnware", methods=["GET"])
def search_learnware():
    result = {
        "code": 0,
        "msg": "Ok",
        # "data": C.engine.get_property_list(),
    }
    return jsonify(result)


@engine_api.route("/download_learnware", methods=["GET"])
@login_required
def download_learnware():
    learnware_name = "file.zip"
    learnware_path = os.path.join(C.root_path, "files")
    response = make_response(send_from_directory(learnware_path, learnware_name, as_attachment=True))
    return response
