"""
"""
import context
import requests


def add_learnware_verified(learnware_id, check_status):
    host = context.config["backend_host"]
    port = context.config["listen_port"]
    url = f"http://{host}:{port}/user/add_learnware_verified"
    data = {"learnware_id": learnware_id, "check_status": check_status}

    response = requests.post(url, json=data)

    if response.status_code != 200:
        raise Exception(f"Add learnware verified failed: {response.text}")

    result = response.json()

    if result["code"] != 0:
        raise Exception(f"Add learnware verified failed: {result['msg']}")

    return result


def get_learnware(learnware_id):
    host = context.config["backend_host"]
    port = context.config["listen_port"]
    url = f"http://{host}:{port}/engine/get_learnware"
    data = {"learnware_id": learnware_id}

    response = requests.get(url, params=data)

    if response.status_code != 200:
        raise Exception(f"Get learnware dirpath failed: {response.text}")

    result = response.json()

    if result["code"] != 0:
        raise Exception(f"Get learnware dirpath failed: {result['msg']}")

    return result["data"]["learnware_dirpath"], result["data"]["semantic_specification"]
