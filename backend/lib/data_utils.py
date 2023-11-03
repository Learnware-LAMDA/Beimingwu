import context
from database.base import LearnwareVerifyStatus
import json


def get_learnware_semantic_specification(learnware_info: dict):
    learnware_id = learnware_info["learnware_id"]
    learnware = context.engine.get_learnware_by_ids(learnware_id)

    if learnware is not None:
        semantic_specification = learnware.get_specification().get_semantic_spec()
    else:
        semantic_spec_path = context.get_learnware_verify_file_path(learnware_id)[:-4] + ".json"
        with open(semantic_spec_path, "r") as f:
            semantic_specification = json.load(f)

    return semantic_specification
