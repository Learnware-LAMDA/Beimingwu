import context
from context import config as C

from learnware import market, specification
from learnware.market.heterogeneous import utils as learnware_utils
from flask import jsonify, g
from datetime import datetime, timedelta
from collections import defaultdict
import functools
import os, json, time
import hashlib
import traceback
import tempfile
import zipfile
import learnware.config
import yaml
from learnware.learnware.utils import get_stat_spec_from_config
from learnware.config import C as learnware_config
from . import common_utils
from . import sensitive_words_utils
import uuid
import shutil


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
    """get learnware by ids

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
        learneare_list.append(
            {
                "learnware_id": id,
                "semantic_specification": learnware.get_specification().get_semantic_spec(),
            }
        )
    return learneare_list


def search_learnware(semantic_specification, statistical_str, user_id, check_status=None):
    # Load statistical specification
    # statistical_name = f"{int(time.time())}_" + hashlib.md5(statistical_str).hexdigest() + ".json"
    statistical_name = uuid.uuid4().hex + ".json"
    statistical_path = os.path.join(C.upload_path, statistical_name)

    # Define statistical specification
    statistical_specification = None
    statistical_specification_type = ""
    context.logger.info(specification.__dict__)
    statistical_specification_dict = {
        "RKMETableSpecification": specification.RKMETableSpecification(),
        "RKMEImageSpecification": specification.RKMEImageSpecification(),
        "RKMETextSpecification": specification.RKMETextSpecification(),
    }

    try:
        with open(statistical_path, "wb") as stats:
            stats.write(statistical_str)

        with open(statistical_path, "r") as f:
            data = json.load(f)
            statistical_specification_type = data.get("type", "RKMETableSpecification")

        statistical_specification = statistical_specification_dict[statistical_specification_type]
        statistical_specification.load(statistical_path)
    except:
        os.remove(statistical_path)
        return False, "Statistical specification error.", None
    if statistical_specification is None:
        os.remove(statistical_path)
        return False, f"Statistical specification error.", None
    os.remove(statistical_path)

    # Search Learnware
    user_info = market.BaseUserInfo(
        id=user_id,
        semantic_spec=semantic_specification,
        stat_info={statistical_specification_type: statistical_specification},
    )

    try:
        context.logger.info(f"stat_info in user: {user_info.stat_info}")
        is_hetero = learnware_utils.is_hetero(stat_specs=user_info.stat_info, semantic_spec=user_info.semantic_spec)
        search_result = context.engine.search_learnware(user_info, check_status=check_status)
    except Exception as err:
        print(err)
        traceback.print_exc()
        return False, "Engine search learnware error.", None

    single_result = search_result.get_single_results()
    multiple_result = search_result.get_multiple_results()

    matching = [single_item.score for single_item in single_result]
    single_learnware_list = [single_item.learnware for single_item in single_result]
    multi_score = None if len(multiple_result) == 0 else multiple_result[0].score
    multi_learnware = [] if len(multiple_result) == 0 else multiple_result[0].learnwares
    # Return learnware
    return True, "", (matching, single_learnware_list, multi_score, multi_learnware, is_hetero)


def search_learnware_by_semantic(semantic_specification, user_id, check_status=None):
    # Search Learnware
    info = market.BaseUserInfo(
        id=user_id,
        semantic_spec=semantic_specification,
        stat_info={},  # No statistical specification
    )
    try:
        search_result = context.engine.search_learnware(info, check_status=check_status)
    except Exception as err:
        return False, f"Engine search learnware error.", None

    # Return learnware
    single_result = search_result.get_single_results()
    single_learnware_list = [single_item.learnware for single_item in single_result]
    return True, "", (None, single_learnware_list, 0.0, None)


def parse_semantic_specification(semantic_str):
    try:
        semantic_specification = json.loads(semantic_str)
    except:
        return None, "Semantic specification error"

    data_type_values = semantic_specification["Data"]["Values"]
    if len(data_type_values) != 1:
        return None, "data type values is not 1"

    data_type = data_type_values[0]

    if data_type == "Table":
        data_input = semantic_specification["Input"]
        if isinstance(data_input, str):
            try:
                data_input = json.loads(data_input)
            except:
                return None, "Input section of semantic is not a json"
        elif isinstance(data_input, dict):
            pass
        else:
            return None, "Input section of semantic is not a json or dict"

        dimension = data_input.get("Dimension")
        if dimension is None:
            return None, "Input has no dimension"

        semantic_specification["Input"] = data_input
        pass
    else:
        # should we check other data type?
        semantic_specification["Input"] = {}
        pass

    task_type_values = semantic_specification["Task"]["Values"]
    if len(task_type_values) != 1:
        return None, "Output is not 1"

    task_type = task_type_values[0]
    if task_type in ("Classification", "Regression"):
        task_output = semantic_specification["Output"]
        if isinstance(task_output, str):
            try:
                task_output = json.loads(task_output)
            except:
                return None, "Output section of semantic is not a json"
        elif isinstance(task_output, dict):
            pass
        else:
            return None, "Output section of semantic is not a json or dict"

        dimension = task_output.get("Dimension")
        if dimension is None:
            return None, "Output has no dimension"

        semantic_specification["Output"] = task_output
        pass
    else:
        # should we check other task type?
        semantic_specification["Output"] = {}
        pass

    return (
        semantic_specification,
        "",
    )


def check_semantic_spec(semantic_specification):
    try:
        # Check semantic_specification
        result, msg = market.EasySemanticChecker.check_semantic_spec(semantic_specification)
        if result == market.EasySemanticChecker.INVALID_LEARNWARE:
            return False, msg

        # Name length check
        if len(semantic_specification["Name"]["Values"]) < 5:
            return False, f"Name length is less than 5"
        if len(semantic_specification["Name"]["Values"]) > 50:
            return False, f"Name length is more than 50"

        # Description length check
        if len(semantic_specification["Description"]["Values"]) < 10:
            return False, f"Description length is less than 10"
        if len(semantic_specification["Description"]["Values"]) > 10000:
            return False, f"Description length is more than 10000"

        # Check sensitive words
        if context.sensitive_pattern is not None:
            sub_semantic = semantic_specification.copy()
            sub_semantic["Input"] = {}
            sub_semantic["Output"] = {}
            semantic_str = json.dumps(semantic_specification, ensure_ascii=False)
            matches = sensitive_words_utils.search_sensitive_words(semantic_str, context.sensitive_pattern)
            if len(matches) > 0:
                return False, f"Sensitive words {','.join(matches)} in semantic specification"

    except Exception as err:
        return False, f"semantic specification error: {err}"

    return True, ""


def check_data_type(semantic_specification, statistical_specification):
    data_type = semantic_specification["Data"]["Values"][0]

    if data_type == "Table":
        if statistical_specification.type != "RKMETableSpecification":
            return False, f"data type does not match statistical specition type"
        else:
            dim_table = int(semantic_specification["Input"]["Dimension"])
            dim_rkme = statistical_specification.get_z().shape[1]
            if dim_table != dim_rkme:
                return False, f"dimension of table is {dim_table}, dimension of rkme is {dim_rkme}"
    elif data_type == "Image":
        if statistical_specification.type != "RKMEImageSpecification":
            return False, f"data type does not match statistical specition type"
    elif data_type == "Text":
        if statistical_specification.type != "RKMETextSpecification":
            return False, f"data type does not match statistical specition type"
    else:
        return False, f"data_type must be in ['Table', 'Image', 'Text']"

    return True, ""


def check_learnware_file(semantic_specification, learnware_file):
    # Check file extension
    suffix = os.path.splitext(learnware_file)[1]

    if suffix != ".zip":
        return False, "learnware file is not a zip file"

    temp_dir = tempfile.TemporaryDirectory(prefix="learnware_check_file_")

    try:
        result, msg = check_semantic_spec(semantic_specification)
        if result == False:
            return result, msg

        with zipfile.ZipFile(learnware_file, "r") as z_file:
            top_folder = common_utils.get_top_folder_in_zip(z_file)

            yaml_file = learnware.config.C.learnware_folder_config["yaml_file"]
            yaml_file = top_folder + yaml_file
            z_file.extract(yaml_file, temp_dir.name)

            with open(os.path.join(temp_dir.name, yaml_file), "r") as fin:
                learnware_config = yaml.safe_load(fin)

            stat_specs = learnware_config.get("stat_specifications")

            if stat_specs is None:
                return False, f"no stat_specifications in {yaml_file}"

            # Check stat_specifications
            for stat_spec in stat_specs:
                member = stat_spec["file_name"]
                member = top_folder + member
                z_file.extract(member, temp_dir.name)
                stat_spec["file_name"] = os.path.join(temp_dir.name, member)
                stat_spec_obj = get_stat_spec_from_config(stat_spec)

                result, msg = check_data_type(semantic_specification, stat_spec_obj)
                if result == False:
                    return result, msg

    except Exception as err:
        return False, f"extract statistical specification error: {err}"

    finally:
        temp_dir.cleanup()

    return True, ""


def get_learnware_count_detail(check_status=None):
    count_detail = dict()
    count_detail["Data"] = defaultdict(int)
    count_detail["Task"] = defaultdict(int)
    count_detail["Library"] = defaultdict(int)
    count_detail["Scenario"] = defaultdict(int)

    for learnware_id in context.engine.get_learnware_ids(check_status=check_status):
        try:
            learnware_obj = context.engine.get_learnware_by_ids(learnware_id)
            semantic_spec = learnware_obj.get_specification().get_semantic_spec()
            for key, value in count_detail.items():
                for v in semantic_spec[key]["Values"]:
                    value[v] += 1
        except Exception as err:
            print(f"load {learnware_id} failed due to {err}!")

    return count_detail


def update_learnware_yaml_file(learnware_path, learnware_id, semantic_spec):
    yaml_file = learnware_config.learnware_folder_config["yaml_file"]
    yaml_file_path = os.path.join(learnware_path, yaml_file)
    with open(yaml_file_path, "r") as f:
        learnware_info = yaml.safe_load(f)
        pass

    with open(os.path.join(learnware_path, "semantic_specification.json"), "w") as fout:
        json.dump(semantic_spec, fout, indent=4)
        pass
    learnware_info["id"] = learnware_id
    learnware_info["semantic_specification"] = {"file_name": "semantic_specification.json"}
    with open(yaml_file_path, "w") as f:
        yaml.dump(learnware_info, f)
        pass
    pass


def repack_learnware_folder(input_zip_path: str, output_path: str, learnware_id: str, semantic_specification: dict):
    """
    Repack learnware: add semantic_specification.json and remove top folder
    """

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    context.logger.info(f"Extracting learnware to {output_path}")
    with zipfile.ZipFile(input_zip_path, "r") as zip_ref:
        top_folder = common_utils.get_top_folder_in_zip(zip_ref)

        if len(top_folder) > 0:
            with tempfile.TemporaryDirectory() as tempdir:
                zip_ref.extractall(tempdir)
                content_path = os.path.join(tempdir, top_folder)
                for file in os.listdir(content_path):
                    shutil.move(os.path.join(content_path, file), os.path.join(output_path, file))
                    pass
                pass
        else:
            zip_ref.extractall(output_path)
            pass

    update_learnware_yaml_file(output_path, learnware_id, semantic_specification)
    pass
