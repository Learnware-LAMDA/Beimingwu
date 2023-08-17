import lib.engine as engine_helper
import json
import flask_jwt_extended
import lib.database_operations as dbops
import zipfile
import tempfile


def add_learnware(learnware_path, semantic_specification, learnware_id):
    learnware_semantic_spec_path = learnware_path[:-4] + ".json"

    # check learnware file
    check_result, msg = engine_helper.check_learnware_file(
        semantic_specification, learnware_path)

    if not check_result:
        return {"code": 51, "msg": msg}, 200
    
    with open(learnware_semantic_spec_path, "w") as f:
        json.dump(semantic_specification, f, indent=4)
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