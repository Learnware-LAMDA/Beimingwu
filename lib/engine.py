from config import C
from learnware.learnware import Learnware
from learnware import market, specification
from flask import jsonify, g
from datetime import datetime, timedelta
import functools
import os, json, time
import hashlib

def cache(seconds: int, maxsize: int = 128, typed: bool = False):
    def wrapper_cache(func):
        func = functools.lru_cache(maxsize=maxsize, typed=typed)(func)
        func.delta = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.delta

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.delta

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache

def get_learnware_by_id(ids):
    """ get learnware by ids

    Args:
        ids (_type_): _description_

    Returns:
        _type_: _description_
    """
    ret = C.engine.get_learnware_by_ids(ids)
    learneare_list = []
    for id, learnware in zip(ids, ret):
        if learnware == None:
            continue
        learneare_list.append({
            "learnware_id": id,
            "semantic_specification": learnware.get_specification().get_semantic_spec(),
        })
    return learneare_list 

@cache(seconds=600, maxsize=1024)
def cached_search_learnware(semantic_str, statistical_str):
    print("Search")
    
    # Load semantic specification
    try:
        semantic_specification = json.loads(semantic_str)
    except:
        return False, jsonify({"code": 51, "msg": "Semantic specification error"}), None
    
    # Load statistical specification
    statistical_name = f"{int(time.time())}_" + hashlib.md5(statistical_str).hexdigest() + ".json"
    statistical_path = os.path.join(C.upload_path, statistical_name)
    statistical_specification = None
    try:
        with open(statistical_path, "wb") as stats:
            stats.write(statistical_str)
        statistical_specification = specification.rkme.RKMEStatSpecification()
        statistical_specification.load(statistical_path)
    except:
        os.remove(statistical_path)
        return False, jsonify({"code": 41, "msg": f"Statistical specification error."}), None
    if statistical_specification is None:
        os.remove(statistical_path)
        return False, jsonify({"code": 41, "msg": f"Statistical specification error."}), None
    os.remove(statistical_path)
    
    # Search Learnware
    info = market.BaseUserInfo(
        id = None if g.user is None else str(g.user['id']),
        semantic_spec=semantic_specification,
        stat_info={"RKMEStatSpecification": statistical_specification},
    )
    try:
        matching, single_learnware_list, multi_learnware = C.engine.search_learnware(info)
    except:
        return False, jsonify({"code": 42, "msg": f"Engine search learnware error."}), None
    
    # Return learnware
    return True, "", (matching, single_learnware_list, multi_learnware)

@cache(seconds=600, maxsize=1024)
def cached_search_learnware_by_semantic(semantic_str):
    # Load semantic specification
    try:
        semantic_specification = json.loads(semantic_str)
    except:
        return False, jsonify({"code": 51, "msg": "Semantic specification error"}), None
    
    # Search Learnware
    info = market.BaseUserInfo(
        id = None if g.user is None else str(g.user['id']),
        semantic_spec=semantic_specification,
        stat_info={}, # No statistical specification
    )
    try:
        matching, single_learnware_list, multi_learnware = C.engine.search_learnware(info)
    except:
        return False, jsonify({"code": 42, "msg": f"Engine search learnware error."}), None
    
    # Return learnware
    return True, "", (matching, single_learnware_list, multi_learnware)