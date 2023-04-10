from flask import Blueprint, jsonify, request
from flask import send_from_directory, send_file, make_response, g
from .auth import login_required
from config import C
import os, json, time
import hashlib
from learnware import market, specification
from .utils import dump_learnware
engine_api = Blueprint("Engine-API", __name__)


@engine_api.route("/get_semantic_specification", methods=["GET"])
def get_semantic_specification():
    result = {
        "code": 0,
        "msg": "Ok",
        "data": {
            "semantic_specification": C.engine.get_semantic_spec_list()
        }
    }
    return jsonify(result)


@engine_api.route("/search_learnware", methods=["POST"])
def search_learnware():
    # Load name & semantic specification
    semantic_specification = request.form.get("semantic_specification")
    if 'statistical_specification' not in request.files or semantic_specification is None:
        return jsonify({"code": 21, "msg": f"Request parameters error."})
    try:
        semantic_specification = json.loads(semantic_specification)
    except:
        return jsonify({"code": 41, "msg": "Semantic specification error"})
    
    # Check statistical specification
    statistical_file = request.files['statistical_specification']
    if statistical_file.filename == '' or not statistical_file:
        return jsonify({"code": 21, "msg": f"Request parameters error."})
    
    # Load statistical specification
    print(statistical_file)
    statistical_name = f"{int(time.time())}_" + hashlib.md5(statistical_file.read()).hexdigest() + ".json"
    statistical_file.seek(0)
    statistical_path = os.path.join(C.upload_path, statistical_name)
    statistical_file.save(statistical_path)
    statistical_specification = None
    try:
        # with open(statistical_path, "r") as f:
        statistical_specification = specification.rkme.RKMEStatSpecification()
        statistical_specification.load(statistical_path)
            # statistical_specification = json.loads(f.read())
    except:
        return jsonify({"code": 42, "msg": f"Statistical specification error."})
    if statistical_specification is None:
        return jsonify({"code": 42, "msg": f"Statistical specification error."})
    
    # Search Learnware
    info = market.BaseUserInfo(
        id=g.user['id'],
        semantic_spec=semantic_specification,
        stat_info={"RKMEStatSpecification": statistical_specification},
    )
    matching, single_learnware_list, multi_learnware = C.engine.search_learnware(info)
    print("="*50)
    print(matching)
    print("="*50)
    print(single_learnware_list)
    print("="*50)
    print(multi_learnware)
    print("="*50)
    assert len(matching) == len(single_learnware_list)
    n = len(single_learnware_list)
    
    # Directly whole list
    result = {
        "code": 0,
        "msg": "Ok",
        "data": {
            "multi": [dump_learnware(x) for x in multi_learnware],
            "single": [dump_learnware(single_learnware_list[i], matching[i]) for i in range(n)],
        }
    }
    return jsonify(result)


@engine_api.route("/download_learnware", methods=["GET"])
@login_required
def download_learnware():
    learnware_name = "file.zip"
    learnware_path = os.path.join(C.root_path, "files")
    response = make_response(send_from_directory(learnware_path, learnware_name, as_attachment=True))
    return response
