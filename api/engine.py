from flask import Blueprint, jsonify, request
from config import C

engine_api = Blueprint("Engine-API", __name__)


@engine_api.route("/get_semantic_specification", methods=["GET"])
def get_semantic_specification():
    result = {
        "code": 0, 
        "msg": "Ok",
        "data": C.engine.get_property_list(),
    }
    return jsonify(result)
