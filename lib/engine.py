import context
from context import config as C

from learnware import market, specification
from flask import jsonify, g
from datetime import datetime, timedelta
import functools
import os, json, time
import hashlib
import traceback
import tempfile
import zipfile
import learnware.config
import yaml
from learnware.learnware.utils import get_stat_spec_from_config


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
        if isinstance(data_input, str):
            try:
                data_input = json.loads(data_input)
            except:
                return None, "Input section of semantic is not a json"
        elif isinstance(data_input, dict):
            pass
        else:
            return None, "Input section of semantic is not a json or dict"
        
        dimension = data_input.get('Dimension')
        if dimension is None:
            return None, "Input has no dimension"
        
        semantic_specification['Input'] = data_input
        pass
    else:
        # should we check other data type?
        semantic_specification['Input'] = {}
        pass
    
    task_type_values = semantic_specification['Task']['Values']
    if len(task_type_values) != 1:
        return None, "Output is not 1"
    
    task_type = task_type_values[0]
    if task_type in ('Classification', 'Regression', 'Feature Extraction'):
        task_output = semantic_specification['Output']
        if isinstance(task_output, str):
            try:
                task_output = json.loads(task_output)
            except:
                return None, "Output section of semantic is not a json"
        elif isinstance(task_output, dict):
            pass
        else:
            return None, "Output section of semantic is not a json or dict"
        
        dimension = task_output.get('Dimension')
        if dimension is None:
            return None, "Output has no dimension"
        
        semantic_specification['Output'] = task_output
        pass
    else:
        # should we check other task type?
        semantic_specification['Output'] = {}
        pass

    return semantic_specification, "",


def check_learnware_file(semantic_specification, learnware_file):
    # Check file extension
    suffix = os.path.splitext(learnware_file)[1]

    if suffix != ".zip":
        return False, "learnware file is not a zip file"
    
    temp_dir = tempfile.TemporaryDirectory(prefix="learnware_check_file_")

    try:
        yaml_file = learnware.config.C.learnware_folder_config["yaml_file"]

        with zipfile.ZipFile(learnware_file, "r") as z_file:
            z_file.extract(yaml_file, temp_dir.name)

            with open(os.path.join(temp_dir.name, yaml_file), "r") as fin:
                learnware_config = yaml.safe_load(fin)
                pass

            stat_specs = learnware_config.get("stat_specifications")

            if stat_specs is None:
                return False, f"no stat_specifications in {yaml_file}"

            for stat_spec in stat_specs:
                member = stat_spec["file_name"]
                z_file.extract(member, temp_dir.name)
                stat_spec["file_name"] = os.path.join(temp_dir.name, stat_spec["file_name"])
                stat_spec_name, stat_spec_obj = get_stat_spec_from_config(stat_spec)

                if stat_spec_name == 'RKMEStatSpecification':
                    if semantic_specification['Data']['Values'][0] == 'Table':
                        dim_table = int(semantic_specification['Input']['Dimension'])
                        dim_rkme = stat_spec_obj.get_z().shape[1]
                        if dim_table != dim_rkme:
                            return False, f"dimension of table is {dim_table}, dimension of rkme is {dim_rkme}"
                        pass
                    pass
                pass
            pass
        pass
    except Exception as err:
        return False, f"extract statistical specification error: {err}"
    finally:
        temp_dir.cleanup()

    
    return True, ""