import context
from context import config as C

from learnware.learnware import Learnware
from learnware import market, specification
from flask import jsonify, g
from datetime import datetime, timedelta
import functools
import os, json, time
import hashlib
import traceback


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
    ret = context.engine.get_learnware_by_ids(ids)
    learneare_list = []
    for id, learnware in zip(ids, ret):
        if learnware == None:
            continue
        learneare_list.append({
            "learnware_id": id,
            "semantic_specification": learnware.get_specification().get_semantic_spec(),
        })
    return learneare_list 


def search_learnware(semantic_str, statistical_str, user_id):
    # Load semantic specification
    try:
        semantic_specification = json.loads(semantic_str)
    except:
        return False, "Semantic specification error", None
    
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
        return False, "Statistical specification error.", None
    if statistical_specification is None:
        os.remove(statistical_path)
        return False, f"Statistical specification error.", None
    os.remove(statistical_path)
    
    # Search Learnware
    info = market.BaseUserInfo(
        id = user_id,
        semantic_spec=semantic_specification,
        stat_info={"RKMEStatSpecification": statistical_specification},
    )
    try:
        matching, single_learnware_list, multi_score, multi_learnware = context.engine.search_learnware(info)
    except Exception as err:
        print(err)
        traceback.print_exc()
        return False, "Engine search learnware error.", None
    
    # Return learnware
    return True, "", (matching, single_learnware_list, multi_score, multi_learnware)


def search_learnware_by_semantic(semantic_str, user_id):
    # Load semantic specification
    try:
        semantic_specification = json.loads(semantic_str)
    except:
        return False, "Semantic specification error", None
    
    # Search Learnware
    info = market.BaseUserInfo(
        id = user_id,
        semantic_spec=semantic_specification,
        stat_info={}, # No statistical specification
    )
    try:
        matching, single_learnware_list, multi_score, multi_learnware = context.engine.search_learnware(info)
    except Exception as err:
        return False, f"Engine search learnware error.", None
    
    # Return learnware
    return True, "", (matching, single_learnware_list, multi_score, multi_learnware)


def parse_semantic_specification(semantic_str):
    try:
        semantic_specification = json.loads(semantic_str)
    except:
        return None, "Semantic specification error"
    
    data_type_values = semantic_specification['Data']['Values']
    if len(data_type_values) != 1:
        return None, "data type values is not 1"
    
    data_type = data_type_values[0]

    if data_type == 'Table':
        data_input = semantic_specification['Input']
        try:
            data_input = json.loads(data_input)
        except:
            return None, "data type description is not a json"
        
        dimension = data_input.get('Dimension')
        if dimension is None:
            return None, "data type description has no dimension"
        
        semantic_specification['Input'] = data_input
        pass
    else:
        # should we check other data type?
        pass
    
    task_type_values = semantic_specification['Task']['Values']
    if len(task_type_values) != 1:
        return None, "task type values is not 1"
    
    task_type = task_type_values[0]
    if task_type in ('Classification', 'Regression', 'Feature Extraction'):
        task_output = semantic_specification['Output']
        try:
            task_output = json.loads(task_output)
        except:
            return None, "task type description is not a json"
        
        dimension = task_output.get('Dimension')
        if dimension is None:
            return None, "task type description has no dimension"
        
        semantic_specification['Output'] = task_output
        pass

    return semantic_specification, "",