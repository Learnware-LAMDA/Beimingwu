import io
import zipfile
from flask import Blueprint, Response, jsonify, request
from flask import send_from_directory, send_file, make_response, g
from .auth import login_required
from config import C
import os, json, time
import hashlib
from learnware import market, specification
from .utils import dump_learnware, get_parameters
engine_api = Blueprint("Engine-API", __name__)


@engine_api.route("/get_semantic_specification", methods=["GET"])
def get_semantic_specification():
    try:
        result = {
            "code": 0,
            "msg": "Ok",
            "data": {
                "semantic_specification": C.engine.get_semantic_spec_list()
            }
        }
        return jsonify(result)
    except:
        return jsonify({"code": 41, "msg": "Engine get semantic specification error."})


@engine_api.route("/search_learnware", methods=["POST"])
def search_learnware():
    # Load name & semantic specification
    semantic_specification = request.form.get("semantic_specification")
    if 'statistical_specification' not in request.files or semantic_specification is None:
        return jsonify({"code": 21, "msg": f"Request parameters error."})
    try:
        semantic_specification = json.loads(semantic_specification)
    except:
        return jsonify({"code": 51, "msg": "Semantic specification error"})
    
    # Check statistical specification
    statistical_file = request.files['statistical_specification']
    if statistical_file.filename == '' or not statistical_file:
        return jsonify({"code": 21, "msg": f"Request parameters error."})
    
    # Load statistical specification
    statistical_name = f"{int(time.time())}_" + hashlib.md5(statistical_file.read()).hexdigest() + ".json"
    statistical_file.seek(0)
    statistical_path = os.path.join(C.upload_path, statistical_name)
    statistical_file.save(statistical_path)
    statistical_specification = None
    try:
        statistical_specification = specification.rkme.RKMEStatSpecification()
        statistical_specification.load(statistical_path)
    except:
        return jsonify({"code": 41, "msg": f"Statistical specification error."})
    if statistical_specification is None:
        return jsonify({"code": 41, "msg": f"Statistical specification error."})
    
    # Search Learnware
    info = market.BaseUserInfo(
        id = None if g.user is None else str(g.user['id']),
        semantic_spec=semantic_specification,
        stat_info={"RKMEStatSpecification": statistical_specification},
    )
    try:
        matching, single_learnware_list, multi_learnware = C.engine.search_learnware(info)
    except:
        return jsonify({"code": 42, "msg": f"Engine search learnware error."})
    assert len(matching) == len(single_learnware_list)
    n = len(single_learnware_list)
    
    # Directly whole list
    result = {
        "code": 0,
        "msg": "Ok",
        "data": {
            "learnware_list_multi": [dump_learnware(x) for x in multi_learnware],
            "learnware_list_single": [dump_learnware(single_learnware_list[i], matching[i]) for i in range(n)],
        }
    }
    return jsonify(result)


@engine_api.route("/download_learnware", methods=["GET"])
@login_required
def download_learnware():
    data = get_parameters(request, ["learnware_id"])
    if data is None:
        return jsonify({"code": 21, "msg": "Request parameters error."})
    
    learnware_id = data["learnware_id"]
    try:
        learnware_zip_path = C.engine.get_learnware_path_by_ids(learnware_id)
    except:
        return jsonify({"code": 42, "msg": "Engine download learnware error."})
    
    if learnware_zip_path is None:
        return jsonify({"code": 41, "msg": "Learnware not found."})

    zip_directory = os.path.dirname(learnware_zip_path)
    zip_filename = os.path.basename(learnware_zip_path)    
    response = make_response(send_from_directory(zip_directory, zip_filename, as_attachment=True))

    return response