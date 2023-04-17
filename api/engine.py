import io
import zipfile
from flask import Blueprint, Response, jsonify, request
from flask import send_from_directory, send_file, make_response, g
from .auth import login_required
from config import C
import os, json, time
import hashlib
from learnware import market, specification
import lib.engine as adv_engine
from .utils import dump_learnware, get_parameters, generate_random_str
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
    semantic_str = request.form.get("semantic_specification")
    if 'statistical_specification' not in request.files or semantic_str is None:
        return jsonify({"code": 21, "msg": f"Request parameters error."})
    
    # Check statistical specification
    statistical_file = request.files['statistical_specification']
    if statistical_file.filename == '' or not statistical_file:
        return jsonify({"code": 21, "msg": f"Request parameters error."})

    # Load statistical specification
    statistical_str = statistical_file.read()
    
    # Cached search learnware
    status, msg, ret = adv_engine.cached_search_learnware(semantic_str, statistical_str)
    if not status: return msg
    (matching, single_learnware_list, multi_learnware) = ret
    assert len(matching) == len(single_learnware_list)
    n = len(single_learnware_list)
    
    # Try paging
    limit = request.form.get("limit")
    page  = request.form.get("page")
    try:
        limit = int(limit)
    except:
        limit = None
        
    # Directly whole list
    if limit is None:
        result = {
            "code": 0,
            "msg": "Ok",
            "data": {
                "learnware_list_multi": [dump_learnware(x) for x in multi_learnware],
                "learnware_list_single": [dump_learnware(single_learnware_list[i], matching[i]) for i in range(n)],
            }
        }
        return jsonify(result)
    
    # Paging
    if limit == 0:
        return jsonify({"code": 52, "msg": "Limit cannot be 0."})
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
            "page": page,
            "limit": limit,
            "total_pages": (n + limit - 1) // limit
        }
    }
    if page == 0: 
        result["data"]["learnware_list_multi"] = [dump_learnware(x) for x in multi_learnware]
    result["data"]["learnware_list_single"] = [
        dump_learnware(single_learnware_list[i], matching[i]) 
        for i in range(page * limit, min(n, page * limit + limit))
    ]
    return jsonify(result)
        


@engine_api.route("/download_learnware", methods=["GET"])
def download_learnware():
    learnware_id = request.args.get("learnware_id")

    if learnware_id is None:
        return jsonify({"code": 21, "msg": "Request parameters error."})

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

@engine_api.route("/get_learnware_info", methods=["GET"])
def get_learnware_info():
    data = get_parameters(request, ["learnware_id"])
    learnware_id = data["learnware_id"]

    if learnware_id is None:
        return jsonify({"code": 21, "msg": "Request parameters error."})

    result = {
        "code": 0,
        "msg": "Ok",
        
    }

    return jsonify(result)

@engine_api.route("/download_multi_learnware", methods=["GET"])
def download_multi_learnware():
    data = get_parameters(request, ["learnware_ids"])
    learnware_ids = data["learnware_ids"]
    if learnware_ids is None or not isinstance(learnware_ids, list):
        return jsonify({"code": 21, "msg": "Request parameters error."})
    
    try:
        learnware_paths = [ C.engine.get_learnware_path_by_ids(learnware_id) for learnware_id in learnware_ids]
    except:
        return jsonify({"code": 42, "msg": "Engine download learnware error."})
    
    if None in learnware_paths:
        return jsonify({"code": 41, "msg": "Learnware not found."})
    
    zip_filename = f"Multi_{int(time.time())}_" + generate_random_str(16) + ".zip"
    zip_filename = os.path.join(C.upload_path, zip_filename)
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for learnware_path in learnware_paths:
            filename = os.path.basename(learnware_path)
            zip_file.write(learnware_path, arcname=filename)

    res = send_file(zip_filename, as_attachment=True)
    os.remove(zip_filename)
    return res