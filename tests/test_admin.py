
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
import zipfile


class TestAdmin(unittest.TestCase):

    def setUpClass() -> None:
        unittest.TestCase.setUpClass()
        TestAdmin.server_process = multiprocessing.Process(target=main.main)
        TestAdmin.server_process.start()
        testops.wait_port_open(C.listen_port, 10)
        context.init_database()
        testops.clear_db()
        TestAdmin.user_id = testops.url_request(
            'auth/register', 
            {'username': 'test', 'password': 'test', "email": "test@localhost"})['data']['user_id']
        TestAdmin.learnware_id = testops.add_test_learnware('test@localhost', 'test')

    def tearDownClass() -> None:
        unittest.TestCase.tearDownClass()
        TestAdmin.server_process.kill()
        pass

    
    def test_list_user(self, ):
        headers = testops.login('admin@localhost', 'admin')
        result = testops.url_request(
            'admin/list_user', 
            {'page': 0, 'limit': 10}, headers=headers)

        self.assertEqual(result['code'], 0)
        self.assertEqual(len(result['data']['user_list']), 2)
        
        pass

    
    def test_delete_user(self, ):
        headers = testops.login('admin@localhost', 'admin')
        result = testops.url_request(
            'admin/delete_learnware',
            {'learnware_id': TestAdmin.learnware_id},
            headers=headers)

        self.assertEqual(result['code'], 0)

        result = testops.url_request(
            'admin/delete_user', 
            {'user_id': TestAdmin.user_id}, headers=headers)

        self.assertEqual(result['code'], 0)

        result = testops.url_request(
            'admin/list_user', 
            {'page': 0, 'limit': 10}, headers=headers)
        
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['data']['user_list'][0]['username'], 'admin')
        self.assertEqual(len(result['data']['user_list']), 1)

        testops.url_request(
            'auth/register', 
            {'username': 'test', 'password': 'test', "email": "test@localhost"})
        
        TestAdmin.learnware_id = testops.add_test_learnware('test@localhost', 'test')

        pass


if __name__ == '__main__':
    unittest.main()

