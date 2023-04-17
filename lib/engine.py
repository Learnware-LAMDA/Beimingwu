from config import C
from learnware.learnware import Learnware
from learnware import market, specification
import functools
import time

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

@functools.lru_cache(maxsize=2048)
def cached_search_learnware(semantic_str, statistical_str):
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
        with open(statistical_path, "w") as stats:
            stats.write(statistical_str)
        statistical_specification = specification.rkme.RKMEStatSpecification()
        statistical_specification.load(statistical_path)
    except:
        return False, jsonify({"code": 41, "msg": f"Statistical specification error."}), None
    if statistical_specification is None:
        return False, jsonify({"code": 41, "msg": f"Statistical specification error."}), None
    
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