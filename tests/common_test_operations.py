import lib.database_operations as dbops
import context
import socket
import time
import requests
from context import config as C
import json
import os
from database.base import LearnwareVerifyStatus


def clear_db():
    context.database.execute("DELETE FROM tb_user WHERE username != 'admin'")
    context.database.execute("DELETE FROM tb_user_learnware_relation")
    pass


def check_port_open(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex(('127.0.0.1',port))
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
    
    time.sleep(1)
    pass


def url_request(
        url_path: str, parameters: dict=None, headers=None, return_response=False, files=None, data=None, 
        method='post'):
    url = f'http://127.0.0.1:{C.listen_port}/{url_path}'
    
    if method == 'get':
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


def login(email, password):
    result = url_request(
        'auth/login',
        {'email': email, 'password': password})

    if 'token' not in result['data']:
        raise Exception('login failed: ' + json.dumps(result))
    
    token = result['data']['token']
    headers = {'Authorization': f'Bearer {token}'}
    return headers


def test_learnware_semantic_specification():
    semantic_specification = dict()

    semantic_specification["Data"] = {"Type": "Class", "Values": ["Image"]}
    semantic_specification["Task"] = {"Type": "Class", "Values": ["Detection"]}
    semantic_specification["Library"] = {"Type": "Class", "Values": ["Scikit-learn"]}
    semantic_specification["Scenario"] = {"Type": "Tag", "Values": ["Business"]}
    semantic_specification["Name"] = {"Type": "String", "Values": "Test Classification"}
    semantic_specification["Description"] = {"Type": "String", "Values": "just a test"}

    return semantic_specification


def test_learnware_semantic_specification_ex():
    semantic_specification = dict()

    semantic_specification["Input"] = {}
    semantic_specification["Output"] = {}
    semantic_specification["Data"] = {"Type": "Class", "Values": ["Image"]}
    semantic_specification["Task"] = {"Type": "Class", "Values": ["Detection"]}
    semantic_specification["Library"] = {"Type": "Class", "Values": ["Scikit-learn"]}
    semantic_specification["Scenario"] = {"Type": "Tag", "Values": ["Business"]}
    semantic_specification["Name"] = {"Type": "String", "Values": "Test Classification"}
    semantic_specification["Description"] = {"Type": "String", "Values": "just a test"}

    return semantic_specification


def add_test_learnware(email, password, learnware_filename='test_learnware.zip') -> str:
    headers = login(email, password)
    semantic_specification = test_learnware_semantic_specification_ex()

    learnware_file = open(
        os.path.join('tests', 'data', learnware_filename),'rb')
    files = {'learnware_file': learnware_file}

    # print(semantic_specification)
    result = url_request(
        'user/add_learnware',
        {'semantic_specification': json.dumps(semantic_specification)},
        files=files,
        headers=headers
    )

    learnware_file.close()
    if result['code'] != 0:
        raise Exception('add learnware failed: ' + json.dumps(result))
    
    learnware_id = result['data']['learnware_id']

    dbops.update_learnware_verify_status(learnware_id, LearnwareVerifyStatus.SUCCESS)

    result = url_request(
        'user/add_learnware_verified',
        {'learnware_id': learnware_id},
        headers=headers)
    
    if result['code'] != 0:
        raise Exception('add learnware verified failed: ' + json.dumps(result))

    print(f'added learnware: {learnware_id}')

    return learnware_id


def add_test_learnware_unverified(email, password, learnware_filename='test_learnware.zip') -> str:
    headers = login(email, password)
    semantic_specification = test_learnware_semantic_specification()

    learnware_file = open(
        os.path.join('tests', 'data', learnware_filename),'rb')
    files = {'learnware_file': learnware_file}

    # print(semantic_specification)
    result = url_request(
        'user/add_learnware',
        {'semantic_specification': json.dumps(semantic_specification)},
        files=files,
        headers=headers
    )

    learnware_file.close()
    if result['code'] != 0:
        raise Exception('add learnware failed: ' + json.dumps(result))
    
    learnware_id = result['data']['learnware_id']

    return learnware_id    


def delete_learnware(learnware_id, headers):
    result = url_request(
        'user/delete_learnware',
        {'learnware_id': learnware_id},
        headers=headers
    )

    if result['code'] != 0:
        raise Exception('delete learnware failed: ' + json.dumps(result))
    
    pass