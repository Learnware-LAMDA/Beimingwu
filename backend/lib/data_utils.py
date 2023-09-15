import context
from database.base import LearnwareVerifyStatus
import json


def get_learnware_semantic_specification(learnware_info: dict):
    learnware_id = learnware_info["learnware_id"]
    if learnware_info["verify_status"] == LearnwareVerifyStatus.SUCCESS.value:
        semantic_specification = (
            context.engine.get_learnware_by_ids([learnware_id])[0].get_specification().get_semantic_spec()
        )
    else:
        semantic_spec_path = context.get_learnware_verify_file_path(learnware_id)[:-4] + ".json"
        with open(semantic_spec_path, "r") as f:
            semantic_specification = json.load(f)
            pass
        pass

    return semantic_specification
    pass
