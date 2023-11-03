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
