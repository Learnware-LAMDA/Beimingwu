from typing import Tuple, Any, List, Union, Dict
import random
from learnware import learnware
import lib.database_operations as dbops

__all__ = ["get_parameters", "generate_random_str", "dump_learnware"]


def get_parameters(request, parameters: List[str]) -> bool:
    try:
        data = request.get_json()
    except:
        return None
    for param in parameters:
        if param not in data:
            return None
    return data


def generate_random_str(randomlength: int) -> str:
    random_str = ""
    base_str = "ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789"
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

def dump_learnware(learnware: learnware.Learnware, matching: int=None):
    ret = {
        "learnware_id": learnware.id,
        "username": dbops.get_learnware_owner(learnware.id),
        "semantic_specification": learnware.get_specification().get_semantic_spec(),
    }
    if matching is not None: ret["matching"] = matching
    return ret
