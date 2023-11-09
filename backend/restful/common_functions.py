import lib.engine as engine_helper
import json
import flask_jwt_extended
import lib.database_operations as dbops
from database.base import LearnwareVerifyStatus
from learnware.market import BaseChecker
import context
import os
from lib import redis_utils


def add_learnware(learnware_path, semantic_specification, learnware_id):
    learnware_semantic_spec_path = learnware_path[:-4] + ".json"

    # check learnware file
    check_result, msg = engine_helper.check_learnware_file(semantic_specification, learnware_path)

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


def delete_learnware(user_id, learnware_id):
    print(f"delete learnware: {learnware_id}")

    # Check permission
    learnware_infos, cnt = dbops.get_learnware_list("learnware_id", learnware_id)
    if len(learnware_infos) == 0:
        return {"code": 51, "msg": "Learnware not exist."}, 200

    if learnware_infos[0]["user_id"] != user_id:
        return {"code": 41, "msg": "You do not own this learnware."}, 200

    learnware_info = learnware_infos[0]

    if context.engine.get_learnware_by_ids(learnware_id) is not None:
        ret = context.engine.delete_learnware(learnware_id)
        if not ret:
            return {"code": 42, "msg": "Engine delete learnware error."}, 200
        redis_utils.publish_delete_learnware(learnware_id)
        pass
    else:
        # Delete learnware file
        learnware_path = context.get_learnware_verify_file_path(learnware_id)
        learnware_sematic_spec_path = learnware_path[:-4] + ".json"
        os.remove(learnware_path)
        os.remove(learnware_sematic_spec_path)

    cnt = dbops.remove_learnware("learnware_id", learnware_id)

    result = {"code": 0, "msg": "Delete success."}

    return result, 200
