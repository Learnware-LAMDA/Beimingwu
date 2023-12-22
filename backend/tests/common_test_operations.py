import lib.database_operations as dbops
import context
import socket
import time
import requests
from context import config as C
import json
import os
from database.base import LearnwareVerifyStatus
from learnware.market import BaseChecker
import shutil
import hashlib
from lib import redis_utils
import learnware.config as learnware_conf


def clear_db():
    context.database.execute("DELETE FROM tb_user WHERE username != 'admin'")
    context.database.execute("DELETE FROM tb_user_learnware_relation")
    context.database.execute("DELETE FROM tb_user_token")
    context.database.execute("DELETE FROM tb_log")
    pass


def check_port_open(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex(("127.0.0.1", port))
        if result == 0:
            return True
        else:
            return False
    finally:
        sock.close()
        pass
    pass


def wait_port_open(port, timeout):
    while timeout > 0:
        if check_port_open(port):
            break
        time.sleep(1)
        timeout -= 1
        pass

    if timeout <= 0:
        raise TimeoutError()

    time.sleep(2)
    pass


def url_request(
    url_path: str, parameters: dict = None, headers=None, return_response=False, files=None, data=None, method="post"
):
    url = f"http://127.0.0.1:{C.listen_port}/{url_path}"

    if method == "get":
        response = requests.get(url, params=parameters, headers=headers)
    else:
        if files is None and data is None:
            response = requests.post(url, json=parameters, headers=headers)
        elif data is None:
            response = requests.post(url, data=parameters, files=files, headers=headers)
            pass
        else:
            response = requests.post(url, data=data, files=files, headers=headers)
            pass

    if return_response:
        return response
    else:
        return response.json()
    pass


def login(email, password, hash_password=False):
    if hash_password:
        password = hashlib.md5(password.encode("utf-8")).hexdigest()
        pass

    result = url_request("auth/login", {"email": email, "password": password})

    if result["code"] != 0:
        raise Exception("login failed: " + json.dumps(result))

    if "token" not in result["data"]:
        raise Exception("login failed: " + json.dumps(result))

    token = result["data"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def test_learnware_semantic_specification():
    return test_learnware_semantic_specification_table()


def test_learnware_semantic_specification_table():
    semantic_specification = dict()

    semantic_specification["Input"] = {"Dimension": 64, "Description": {"0": "f0", "1": "f1"}}
    semantic_specification["Output"] = {"Dimension": 10, "Description": {"0": "c0"}}
    semantic_specification["Data"] = {"Type": "Class", "Values": ["Table"]}
    semantic_specification["Task"] = {"Type": "Class", "Values": ["Classification"]}
    semantic_specification["Library"] = {"Type": "Class", "Values": ["Scikit-learn"]}
    semantic_specification["Scenario"] = {"Type": "Tag", "Values": ["Business"]}
    semantic_specification["Name"] = {"Type": "String", "Values": "Test Classification"}
    semantic_specification["Description"] = {"Type": "String", "Values": "just a test"}
    semantic_specification["License"] = {"Type": "Class", "Values": ["Apache-2.0"]}

    return semantic_specification


def add_learnware_to_engine(learnware_id, headers):
    dbops.update_learnware_verify_status(learnware_id, LearnwareVerifyStatus.SUCCESS)
    learnware_file = context.get_learnware_verify_file_path(learnware_id)
    semantic_spec_file = learnware_file[:-4] + ".json"
    with open(semantic_spec_file, "r") as fin:
        semantic_specification = json.load(fin)
        pass

    context.engine.add_learnware(learnware_file, semantic_spec=semantic_specification, learnware_id=learnware_id)
    print(learnware_file)

    redis_utils.publish_reload_learnware(learnware_id)

    os.remove(learnware_file)
    os.remove(semantic_spec_file)
    pass


def add_test_learnware(email, password, learnware_filename="test_learnware.zip") -> str:
    headers = login(email, password)
    semantic_specification = test_learnware_semantic_specification()

    learnware_file = open(os.path.join("tests", "data", learnware_filename), "rb")
    files = {"learnware_file": learnware_file}

    # print(semantic_specification)
    result = url_request(
        "user/add_learnware",
        {"semantic_specification": json.dumps(semantic_specification)},
        files=files,
        headers=headers,
    )

    learnware_file.close()
    if result["code"] != 0:
        raise Exception("add learnware failed: " + json.dumps(result))

    learnware_id = result["data"]["learnware_id"]

    add_learnware_to_engine(learnware_id, headers)

    print(f"added learnware: {learnware_id}")

    return learnware_id


def add_test_learnware_unverified(
    email, password, learnware_filename="test_learnware.zip", semantic_specification=None
) -> str:
    headers = login(email, password)
    if semantic_specification is None:
        semantic_specification = test_learnware_semantic_specification()
        pass

    learnware_file = open(os.path.join("tests", "data", learnware_filename), "rb")
    files = {"learnware_file": learnware_file}

    # print(semantic_specification)
    result = url_request(
        "user/add_learnware",
        {"semantic_specification": json.dumps(semantic_specification)},
        files=files,
        headers=headers,
    )

    learnware_file.close()
    if result["code"] != 0:
        raise Exception("add learnware failed: " + json.dumps(result))

    learnware_id = result["data"]["learnware_id"]

    return learnware_id


def delete_learnware(learnware_id, headers):
    result = url_request("user/delete_learnware", {"learnware_id": learnware_id}, headers=headers)

    if result["code"] != 0:
        raise Exception("delete learnware failed: " + json.dumps(result))

    pass


def download_learnware(learnware_id, headers, download_file):
    result = url_request(
        "engine/download_learnware", {"learnware_id": learnware_id}, headers=headers, return_response=True, method="get"
    )

    if result.status_code != 200:
        raise Exception("download learnware failed: " + json.dumps(result))

    with open(download_file, "wb") as f:
        f.write(result.content)
        pass
    pass


def delete_user(user_id):
    context.database.execute("DELETE FROM tb_user WHERE id = :user_id", {"user_id": user_id})
    pass


def delete_user_by_email(email):
    context.database.execute("DELETE FROM tb_user WHERE email = :email", {"email": email})
    pass


def check_bytes_same(file1: bytearray, file2: bytearray):
    md5_1 = hashlib.md5(file1).hexdigest()
    md5_2 = hashlib.md5(file2).hexdigest()

    return md5_1 == md5_2


def cleanup_folder():
    root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    backend_data_path = os.path.join(root_path, "backend_data")
    learnware_data_path = learnware_conf.ROOT_DIRPATH
    subpaths = ["learnware_pool", "database"]

    if os.path.exists(backend_data_path):
        shutil.rmtree(backend_data_path)

    for subpath in subpaths:
        fullpath = os.path.join(learnware_data_path, subpath)
        if os.path.exists(fullpath):
            shutil.rmtree(fullpath)


def reset_config():
    with open("config.json", "w") as fout:
        json.dump({}, fout, indent=4)
        pass
    pass


def set_config(key, value):
    C.update({key: value})
    with open("config.json", "w") as fout:
        json.dump(C.__dict__["_config"], fout, indent=4)
        pass
    pass
