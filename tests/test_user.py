
import unittest
import main
import multiprocessing
from config import C
import context
import requests
import os
import shutil
from tests import common_test_operations as testops
import time
import json


class TestUser(unittest.TestCase):

    def setUpClass() -> None:
        unittest.TestCase.setUpClass()
        TestUser.server_process = multiprocessing.Process(target=main.main)
        TestUser.server_process.start()
        testops.wait_port_open(C.listen_port, 10)
        context.init_database()
        testops.clear_db()
        TestUser.username = 'test'
        TestUser.email = 'test@localhost'
        TestUser.password = 'test'
        testops.url_request(
            'auth/register', 
            {'username': TestUser.username, 'password': TestUser.password, "email": TestUser.email})


    def tearDownClass() -> None:
        unittest.TestCase.tearDownClass()
        TestUser.server_process.kill()
        pass

    def test_profile(self):
        headers = testops.login(TestUser.email, TestUser.password)
        result = testops.url_request(
            'user/profile', 
            {}, headers=headers)

        self.assertEqual(result['code'], 0)
        self.assertEqual(result['data']['username'], TestUser.username)
        pass
    
    def test_change_password(self):
        headers = testops.login(TestUser.email, TestUser.password)
        result = testops.url_request(
            'user/change_password',
            {'old_password': TestUser.password, 'new_password': 'test2'},
            headers=headers)
        
        self.assertEqual(result['code'], 0)
        
        result = testops.url_request(
            'auth/logout',
            {},
            headers=headers)
        
        self.assertEqual(result['code'], 0)

        headers = testops.login(TestUser.email, 'test2')

        result = testops.url_request(
            'user/change_password',
            {'old_password': 'test2', 'new_password': TestUser.password},
            headers=headers)
        
        self.assertEqual(result['code'], 0)

        pass

    def test_list_learnware(self):
        headers = testops.login(TestUser.email, TestUser.password)
        semantic_specification = dict()

        semantic_specification["Data"] = {"Type": "Class", "Values": ["Table"]}
        semantic_specification["Task"] = {"Type": "Class", "Values": ["Classification"]}
        semantic_specification["Library"] = {"Type": "Class", "Values": ["Scikit-learn"]}
        semantic_specification["Scenario"] = {"Type": "Tag", "Values": ["Business"]}
        semantic_specification["Name"] = {"Type": "String", "Values": ["Test Classification"]}
        semantic_specification["Description"] = {"Type": "String", "Values": ["just a test"]}

        learnware_file = open(
            os.path.join('tests', 'data', 'test_learnware.zip'),'rb')
        files = {'learnware_file': learnware_file}

        # print(semantic_specification)
        result = testops.url_request(
            'user/add_learnware',
            {'semantic_specification': json.dumps(semantic_specification)},
            files=files,
            headers=headers
        )

        learnware_file.close()
        self.assertEqual(result['code'], 0)
        learnware_id = result['data']['learnware_id']

        result = testops.url_request(
            'user/list_learnware',
            {'page': 0, 'limit': 10},
            headers=headers
        )

        self.assertEqual(result['code'], 0)
        self.assertEqual(result['data']['total_pages'], 1)
        self.assertEqual(result['data']['learnware_list'][0]['learnware_id'], learnware_id)

        result = testops.url_request(
            'user/delete_learnware',
            {'learnware_id': learnware_id},
            headers=headers
        )

        self.assertEqual(result['code'], 0)

        result = testops.url_request(
            'user/list_learnware',
            {'page': 0, 'limit': 10},
            headers=headers
        )

        self.assertEqual(result['code'], 0)
        self.assertEqual(len(result['data']['learnware_list']), 0)        

        pass


if __name__ == '__main__':
    unittest.main()

